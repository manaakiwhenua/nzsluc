#!/usr/bin/env python3
"""Generate an OGC SLD style from lu:colour values in the TTL.

Produces one <se:Rule> per classified concept, matching on `lu_code`
directly (plain equality - a QGIS round-trip test showed that a
computed/concatenated filter field silently loses its <ogc:Filter> on SLD
export, matching everything), plus a flat water colour and a flat wetland
colour (no land-use hatch overlay - unlike the QGIS/QML style, SLD has no
clean way to make a symbolizer's colour depend on another attribute
without combinatorial rules).

Usage: export_sld_style.py INPUT.ttl SCHEME_IRI LAYER_NAME OUTPUT.sld
"""
import sys
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
LU = Namespace("https://nzlum.landcareresearch.co.nz/landuse/")

WATER_FILL_HEX = "#43a2ca"
WETLAND_FILL_HEX = "#83B09E"  # matches wtr:swamp/wtr:mangrove in water-features.ttl

SLD_NS = "http://www.opengis.net/sld"
SE_NS = "http://www.opengis.net/se"
OGC_NS = "http://www.opengis.net/ogc"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

ET.register_namespace("", SLD_NS)
ET.register_namespace("se", SE_NS)
ET.register_namespace("ogc", OGC_NS)
ET.register_namespace("xsi", XSI_NS)


def se(tag):
    return f"{{{SE_NS}}}{tag}"


def ogc(tag):
    return f"{{{OGC_NS}}}{tag}"


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


def prop_equals(field, value):
    el = ET.Element(ogc("PropertyIsEqualTo"))
    ET.SubElement(el, ogc("PropertyName")).text = field
    ET.SubElement(el, ogc("Literal")).text = value
    return el


def prop_not_equals(field, value):
    el = ET.Element(ogc("PropertyIsNotEqualTo"))
    ET.SubElement(el, ogc("PropertyName")).text = field
    ET.SubElement(el, ogc("Literal")).text = value
    return el


def prop_is_null(field):
    el = ET.Element(ogc("PropertyIsNull"))
    ET.SubElement(el, ogc("PropertyName")).text = field
    return el


def prop_not(child):
    el = ET.Element(ogc("Not"))
    el.append(child)
    return el


def make_rule(name, filter_children, fill_hex, combinator="And"):
    rule = ET.Element(se("Rule"))
    ET.SubElement(rule, se("Name")).text = name
    desc = ET.SubElement(rule, se("Description"))
    ET.SubElement(desc, se("Title")).text = name

    filt = ET.SubElement(rule, ogc("Filter"))
    if len(filter_children) == 1:
        filt.append(filter_children[0])
    else:
        combo = ET.SubElement(filt, ogc(combinator))
        for child in filter_children:
            combo.append(child)

    symbolizer = ET.SubElement(rule, se("PolygonSymbolizer"))
    fill = ET.SubElement(symbolizer, se("Fill"))
    ET.SubElement(fill, se("SvgParameter"), {"name": "fill"}).text = fill_hex

    return rule


def build_sld(classed, layer_name):
    root = ET.Element(f"{{{SLD_NS}}}StyledLayerDescriptor", {
        "version": "1.1.0",
        f"{{{XSI_NS}}}schemaLocation": f"{SLD_NS} http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd",
    })
    named_layer = ET.SubElement(root, f"{{{SLD_NS}}}NamedLayer")
    ET.SubElement(named_layer, se("Name")).text = layer_name
    user_style = ET.SubElement(named_layer, f"{{{SLD_NS}}}UserStyle")
    ET.SubElement(user_style, se("Name")).text = layer_name
    fts = ET.SubElement(user_style, se("FeatureTypeStyle"))

    for n, lab, col in classed:
        name = f"{n} {lab}"
        fts.append(make_rule(name, [
            prop_equals("lu_code", n),
            prop_is_null("water"),
        ], col))

    fts.append(make_rule("water", [
        prop_not(prop_is_null("water")),
        prop_not_equals("water", "ice"),
        prop_not_equals("water", "swamp"),
        prop_not_equals("water", "mangrove"),
    ], WATER_FILL_HEX))

    fts.append(make_rule("wetland", [
        prop_equals("water", "swamp"),
        prop_equals("water", "mangrove"),
    ], WETLAND_FILL_HEX, combinator="Or"))

    return root


def main():
    if len(sys.argv) != 5:
        print("Usage: export_sld_style.py INPUT.ttl SCHEME_IRI LAYER_NAME OUTPUT.sld", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, layer_name, out_path = sys.argv[1:5]

    classed = load_classed(in_ttl, scheme_iri)
    if not classed:
        raise SystemExit(f"No concepts with lu:colour found in {in_ttl}")

    root = build_sld(classed, layer_name)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")

    with open(out_path, "wb") as f:
        f.write(b"<?xml version='1.0' encoding='UTF-8'?>\n")
        tree.write(f, encoding="utf-8", xml_declaration=False)
        f.write(b"\n")

    print(f"Wrote {out_path} ({len(classed)} classification rules, 2 water rules)", file=sys.stderr)


if __name__ == "__main__":
    main()
