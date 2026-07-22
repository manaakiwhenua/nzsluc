#!/usr/bin/env python3
"""Generate a CartoCSS (.mss) polygon style from lu:colour values in the TTL.

Produces a `::shape` attachment with one attribute-selector rule per
classified concept (matching on `lu_code` directly), plus fixed
(non-TTL-derived) elaborations for water, wetlands, and commodity
presence, and a `::label` attachment for zoom-dependent labelling.

Usage: export_cartocss_style.py INPUT.ttl SCHEME_IRI LAYER_SELECTOR OUTPUT.mss
"""
import sys
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
LU = Namespace("https://nzlum.landcareresearch.co.nz/landuse/")

NULL_FILL_HEX = "#fdffa6"
WATER_FILL_HEX = "#43a2ca"
WETLAND_FILL_HEX = "#83B09E"  # matches wtr:swamp/wtr:mangrove in water-features.ttl


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


def build_cartocss(classed, selector):
    lines = [
        f"{selector} {{",
        "  ::shape {",
        "    polygon-opacity: 0.715;",
        "    line-color: #232323;",
        "    line-width: 0.26;",
        "    line-opacity: 0.1;",
        "",
        "    /* General unspecified/nulled category */",
        f"    [lu_code='NULL'] {{",
        f"      polygon-fill: {NULL_FILL_HEX};",
        "      polygon-opacity: 0.2;",
        "    }",
        "",
    ]
    for n, lab, col in classed:
        lines.append(f"    // {n} {lab}")
        lines.append(f"    [lu_code = '{n}'] {{")
        lines.append(f"      polygon-fill: {col};")
        lines.append("    }")
        lines.append("")

    lines += [
        "    /* Water features, other than ice or wetlands (below) */",
        "    [water!=''][water!='ice'][water!='swamp'][water!='mangrove'] {",
        f"      polygon-fill: {WATER_FILL_HEX};",
        "    }",
        "",
        "    /* Wetlands - coloured separately, matching wtr:swamp/wtr:mangrove",
        "       in rdf/term-lists/water-features.ttl */",
        "    [water='swamp'], [water='mangrove'] {",
        f"      polygon-fill: {WETLAND_FILL_HEX};",
        "    }",
        "",
        "    /* Slightly emphasise parcels with a recorded commodity */",
        "    [commod!=''] {",
        "      polygon-opacity: 0.95;",
        "    }",
        "  }",
        "",
        "  ::label {",
        "    [zoom>14] {",
        "      text-name: [comment];",
        "      text-face-name: 'Open Sans Regular';",
        "      text-avoid-edges: true;",
        "      text-allow-overlap: false;",
        "      text-character-spacing: 0.5;",
        "      text-size: 12;",
        "      text-fill: #fff;",
        "      text-halo-fill: fadeout(black, 40%);",
        "      text-halo-radius: 1;",
        "    }",
        "  }",
        "}",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main():
    if len(sys.argv) != 5:
        print("Usage: export_cartocss_style.py INPUT.ttl SCHEME_IRI LAYER_SELECTOR OUTPUT.mss", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, selector, out_path = sys.argv[1:5]

    classed = load_classed(in_ttl, scheme_iri)
    if not classed:
        raise SystemExit(f"No concepts with lu:colour found in {in_ttl}")

    text = build_cartocss(classed, selector)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Wrote {out_path} ({len(classed)} classification rules)", file=sys.stderr)


if __name__ == "__main__":
    main()
