#!/usr/bin/env python3
"""Generate a QGIS .qml symbology file from lu:colour values in the TTL.

Produces a rule-based renderer with one rule per classified concept
(matching `"lu_code"` directly; the rule's `label` still carries the
canonical "notation label" text so the QGIS legend stays readable), one
rule per water feature value (`"water" = ...`, solid fill in the water
colour with the land-use colour as a hatch overlay on top - looked up via
a data-defined CASE expression rather than combinatorial rules), and a
neutral catch-all.
Built from scratch (no template file) as a symbology-only style
(styleCategories="Symbology"), so loading it in QGIS only replaces the
renderer and leaves the target layer's other settings untouched.

Usage: export_qgis_style.py INPUT.ttl SCHEME_IRI WATER_TTL WATER_SCHEME_IRI OUTPUT.qml
"""
import sys
import uuid
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
LU = Namespace("https://nzlum.landcareresearch.co.nz/landuse/")

DOCTYPE = "<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"

OUTLINE_COLOUR = "35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1"
UNCLASSIFIED_HEX = "#C8C8C8"


def get_en(g, s, p):
    for o in g.objects(s, p):
        if getattr(o, "language", None) == "en":
            return str(o)
    o = next(g.objects(s, p), None)
    return str(o) if o else None


def notation(g, c):
    n = next(g.objects(c, SKOS.notation), None)
    return str(n) if n else None


def colour(g, c):
    n = next(g.objects(c, LU.colour), None)
    return str(n) if n else None


def code_key(code):
    try:
        return [int(x) for x in code.split(".")]
    except Exception:
        return [code]


# Deterministic keys: QGIS only needs rule keys and symbol-layer ids to be unique
# within the style, so derive them from what they identify. Random uuid4 keys
# made every rebuild produce a spurious diff.
GUID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://nzlum.landcareresearch.co.nz/landuse/qgis-style")


def guid(name):
    return "{%s}" % uuid.uuid5(GUID_NAMESPACE, name)


def rgba_value(hex_colour):
    hexpart = hex_colour.lstrip("#")
    r, g, b = (int(hexpart[i:i + 2], 16) for i in (0, 2, 4))
    return f"{r},{g},{b},255,rgb:{r / 255},{g / 255},{b / 255},1"


def load_classed(ttl_path, scheme_iri):
    g = Graph()
    g.parse(ttl_path, format="turtle")
    scheme = URIRef(scheme_iri)
    concepts = [c for c in g.subjects(RDF.type, SKOS.Concept) if (c, SKOS.inScheme, scheme) in g]

    classed = []  # (notation, label, colour)
    for c in concepts:
        col = colour(g, c)
        if not col:
            continue
        n = notation(g, c)
        lab = get_en(g, c, SKOS.prefLabel)
        if not n or not lab:
            continue
        classed.append((n, lab, col))
    classed.sort(key=lambda row: code_key(row[0]))
    return classed


def load_water(ttl_path, scheme_iri):
    g = Graph()
    g.parse(ttl_path, format="turtle")
    scheme = URIRef(scheme_iri)
    concepts = [c for c in g.subjects(RDF.type, SKOS.Concept) if (c, SKOS.inScheme, scheme) in g]

    water = []  # (value, colour)
    for c in concepts:
        col = colour(g, c)
        n = notation(g, c)
        if not col or not n:
            continue
        water.append((n, col))
    water.sort(key=lambda row: row[0])
    return water


def land_colour_case_expression(classed):
    lines = ["CASE"]
    for n, lab, col in classed:
        lines.append(f"  WHEN \"lu_code\" = '{n}' THEN '{col}'")
    lines.append(f"  ELSE '{UNCLASSIFIED_HEX}'")
    lines.append("END")
    return "\n".join(lines)


def add_empty_ddp(parent):
    ddp = ET.SubElement(parent, "data_defined_properties")
    opt = ET.SubElement(ddp, "Option", {"type": "Map"})
    ET.SubElement(opt, "Option", {"value": "", "type": "QString", "name": "name"})
    ET.SubElement(opt, "Option", {"name": "properties"})
    ET.SubElement(opt, "Option", {"value": "collection", "type": "QString", "name": "type"})


def make_symbol(name, layers):
    symbol = ET.Element("symbol", {
        "alpha": "1", "type": "fill", "name": name, "force_rhr": "0",
        "is_animated": "0", "frame_rate": "10", "clip_to_extent": "1",
    })
    add_empty_ddp(symbol)
    for layer in layers:
        symbol.append(layer)
    return symbol


def make_simplefill_layer(symbol_name, colour_value):
    layer = ET.Element("layer", {
        "locked": "0", "pass": "0", "class": "SimpleFill", "enabled": "1", "id": guid(f"{symbol_name}:SimpleFill"),
    })
    lopt = ET.SubElement(layer, "Option", {"type": "Map"})

    def add_opt(name_, value_):
        ET.SubElement(lopt, "Option", {"value": value_, "type": "QString", "name": name_})

    add_opt("border_width_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("color", colour_value)
    add_opt("joinstyle", "bevel")
    add_opt("offset", "0,0")
    add_opt("offset_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("offset_unit", "MM")
    add_opt("outline_color", OUTLINE_COLOUR)
    add_opt("outline_style", "no")
    add_opt("outline_width", "0.26")
    add_opt("outline_width_unit", "MM")
    add_opt("style", "solid")

    add_empty_ddp(layer)
    return layer


def make_linepatternfill_layer(symbol_name, fallback_colour_value, colour_expression):
    """A diagonal-hatch fill layer whose line colour is overridden per-feature
    via a data-defined expression on the nested line symbol's `outlineColor`
    property - verified against a real QGIS-exported example (the colour
    override does not live on the LinePatternFill layer's own `color`
    property; QGIS renders the hatch via an embedded line symbol).
    """
    layer = ET.Element("layer", {
        "locked": "0", "pass": "0", "class": "LinePatternFill", "enabled": "1", "id": guid(f"{symbol_name}:LinePatternFill"),
    })
    lopt = ET.SubElement(layer, "Option", {"type": "Map"})

    def add_opt(name_, value_):
        ET.SubElement(lopt, "Option", {"value": value_, "type": "QString", "name": name_})

    add_opt("angle", "45")
    add_opt("clip_mode", "during_render")
    add_opt("color", fallback_colour_value)
    add_opt("coordinate_reference", "feature")
    add_opt("distance", "2")
    add_opt("distance_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("distance_unit", "MM")
    add_opt("line_width", "0.3")
    add_opt("line_width_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("line_width_unit", "MM")
    add_opt("offset", "0")
    add_opt("offset_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("offset_unit", "MM")
    add_opt("outline_width_map_unit_scale", "3x:0,0,0,0,0,0")
    add_opt("outline_width_unit", "MM")

    add_empty_ddp(layer)

    line_symbol = ET.SubElement(layer, "symbol", {
        "alpha": "1", "type": "line", "name": f"@{symbol_name}@1", "force_rhr": "0",
        "is_animated": "0", "frame_rate": "10", "clip_to_extent": "1",
    })
    add_empty_ddp(line_symbol)

    line_layer = ET.SubElement(line_symbol, "layer", {
        "locked": "0", "pass": "0", "class": "SimpleLine", "enabled": "1", "id": guid(f"{symbol_name}:SimpleLine"),
    })
    slopt = ET.SubElement(line_layer, "Option", {"type": "Map"})

    def add_sl_opt(name_, value_):
        ET.SubElement(slopt, "Option", {"value": value_, "type": "QString", "name": name_})

    add_sl_opt("align_dash_pattern", "0")
    add_sl_opt("capstyle", "square")
    add_sl_opt("customdash", "5;2")
    add_sl_opt("customdash_map_unit_scale", "3x:0,0,0,0,0,0")
    add_sl_opt("customdash_unit", "MM")
    add_sl_opt("dash_pattern_offset", "0")
    add_sl_opt("dash_pattern_offset_map_unit_scale", "3x:0,0,0,0,0,0")
    add_sl_opt("dash_pattern_offset_unit", "MM")
    add_sl_opt("draw_inside_polygon", "0")
    add_sl_opt("joinstyle", "bevel")
    add_sl_opt("line_color", fallback_colour_value)
    add_sl_opt("line_style", "solid")
    add_sl_opt("line_width", "0.3")
    add_sl_opt("line_width_unit", "MM")
    add_sl_opt("offset", "0")
    add_sl_opt("offset_map_unit_scale", "3x:0,0,0,0,0,0")
    add_sl_opt("offset_unit", "MM")
    add_sl_opt("ring_filter", "0")
    add_sl_opt("trim_distance_end", "0")
    add_sl_opt("trim_distance_end_map_unit_scale", "3x:0,0,0,0,0,0")
    add_sl_opt("trim_distance_end_unit", "MM")
    add_sl_opt("trim_distance_start", "0")
    add_sl_opt("trim_distance_start_map_unit_scale", "3x:0,0,0,0,0,0")
    add_sl_opt("trim_distance_start_unit", "MM")
    add_sl_opt("tweak_dash_pattern_on_corners", "0")
    add_sl_opt("use_custom_dash", "0")
    add_sl_opt("width_map_unit_scale", "3x:0,0,0,0,0,0")

    ddp = ET.SubElement(line_layer, "data_defined_properties")
    ddopt = ET.SubElement(ddp, "Option", {"type": "Map"})
    ET.SubElement(ddopt, "Option", {"value": "", "type": "QString", "name": "name"})
    props = ET.SubElement(ddopt, "Option", {"type": "Map", "name": "properties"})
    color_prop = ET.SubElement(props, "Option", {"type": "Map", "name": "outlineColor"})
    ET.SubElement(color_prop, "Option", {"value": "true", "type": "bool", "name": "active"})
    ET.SubElement(color_prop, "Option", {"value": colour_expression, "type": "QString", "name": "expression"})
    ET.SubElement(color_prop, "Option", {"value": "3", "type": "int", "name": "type"})
    ET.SubElement(ddopt, "Option", {"value": "collection", "type": "QString", "name": "type"})

    return layer


def make_rule(label_text, symbol_name, filter_expr):
    attrib = {}
    if label_text is not None:
        attrib["label"] = label_text
    attrib["symbol"] = symbol_name
    attrib["filter"] = filter_expr
    attrib["key"] = guid(f"rule:{filter_expr}")
    return ET.Element("rule", attrib)


def water_filter(value):
    # The template treated 'lake' as a prefix match (LIKE 'lake%'); every
    # other water value was an exact match.
    if value == "lake":
        return f'"water" LIKE \'{value}%\''
    return f'"water" = \'{value}\''


def build_qml(classed, water):
    qgis = ET.Element("qgis", {"styleCategories": "Symbology", "version": "3.42.0"})

    renderer = ET.SubElement(qgis, "renderer-v2", {
        "type": "RuleRenderer", "symbollevels": "0", "forceraster": "0",
        "referencescale": "-1", "enableorderby": "0",
    })
    rules_root = ET.SubElement(renderer, "rules", {"key": guid("rules")})
    symbols_root = ET.SubElement(renderer, "symbols")

    unclassified_rgba = rgba_value(UNCLASSIFIED_HEX)

    # Land-use rules: solid fill, only where there's no water feature.
    for idx, (n, lab, col) in enumerate(classed):
        symbol_name = f"lu{idx}"
        label_text = f"{n} {lab}"
        filter_expr = f"\"lu_code\" = '{n}' AND \"water\" IS NULL"
        rules_root.append(make_rule(label_text, symbol_name, filter_expr))
        symbols_root.append(make_symbol(symbol_name, [make_simplefill_layer(symbol_name, rgba_value(col))]))

    # Water rules: solid water-colour base, land-use colour as a hatch
    # overlay on top (looked up by expression, so this stays 12 rules
    # instead of 39 x 12 combinations).
    hatch_expr = land_colour_case_expression(classed)
    for idx, (value, col) in enumerate(water):
        symbol_name = f"water{idx}"
        rules_root.append(make_rule(value, symbol_name, water_filter(value)))
        symbols_root.append(make_symbol(symbol_name, [
            make_simplefill_layer(symbol_name, rgba_value(col)),
            make_linepatternfill_layer(symbol_name, unclassified_rgba, hatch_expr),
        ]))

    # Catch-all for anything that doesn't match a classified rule, so the
    # renderer degrades visibly (neutral grey) rather than silently.
    rules_root.append(make_rule(None, "unclassified", "ELSE"))
    symbols_root.append(make_symbol("unclassified", [make_simplefill_layer("unclassified", unclassified_rgba)]))

    ET.SubElement(qgis, "blendMode").text = "0"
    ET.SubElement(qgis, "featureBlendMode").text = "0"
    ET.SubElement(qgis, "layerOpacity").text = "1"

    return qgis


def main():
    if len(sys.argv) != 6:
        print("Usage: export_qgis_style.py INPUT.ttl SCHEME_IRI WATER_TTL WATER_SCHEME_IRI OUTPUT.qml", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, water_ttl, water_scheme_iri, out_path = sys.argv[1:6]

    classed = load_classed(in_ttl, scheme_iri)
    if not classed:
        raise SystemExit(f"No concepts with lu:colour found in {in_ttl}")

    water = load_water(water_ttl, water_scheme_iri)
    if not water:
        raise SystemExit(f"No concepts with lu:colour found in {water_ttl}")

    qgis = build_qml(classed, water)
    tree = ET.ElementTree(qgis)
    ET.indent(tree, space="  ")
    xml_text = ET.tostring(qgis, encoding="unicode")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(DOCTYPE)
        f.write(xml_text)
        f.write("\n")

    print(f"Wrote {out_path} ({len(classed)} classification rules, {len(water)} water rules)", file=sys.stderr)


if __name__ == "__main__":
    main()
