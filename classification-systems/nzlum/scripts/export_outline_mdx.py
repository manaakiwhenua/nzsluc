#!/usr/bin/env python3
import sys
import os
from rdflib import Graph, Namespace, URIRef

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def get_en(g, s, p):
    for o in g.objects(s, p):
        if getattr(o, "language", None) == "en":
            return str(o)
    o = next(g.objects(s, p), None)
    return str(o) if o else None

def notation(g, c):
    n = next(g.objects(c, SKOS.notation), None)
    return str(n) if n else ""

def label(g, c):
    return get_en(g, c, SKOS.prefLabel) or ""

def definition(g, c):
    return get_en(g, c, SKOS.definition) or ""

def get_top_concepts(g, scheme):
    return sorted(
        [c for c in g.subjects(SKOS.topConceptOf, scheme)],
        key=lambda c: notation(g, c)
    )

def get_narrower(g, c):
    return sorted(
        [n for n in g.objects(c, SKOS.narrower)],
        key=lambda n: notation(g, n)
    )

def usage_notes(g, c): return all_notes(g, c, SKOS.usageNote)
def scope_notes(g, c): return all_notes(g, c, SKOS.scopeNote)
def change_notes(g, c): return all_notes(g, c, SKOS.changeNote)
def examples(g, c): return all_notes(g, c, SKOS.example)

def all_notes(g, s, p):
    return [str(o) for o in g.objects(s, p) if getattr(o, "language", None) == "en" or not getattr(o, "language", None)]

def render_notes(f, notes, label, type="note", icon=None):
    if notes:
        for note in notes:
            if not icon:
                f.write(f'<Aside type="{type}" title="{label}">\n  {note}\n</Aside>\n\n')
            else:
                f.write(f'<Aside type="{type}" title="{label}" icon="{icon}">\n  {note}\n</Aside>\n\n')

def render_all_notes(f, g, c):
    render_notes(f, scope_notes(g, c), "Scope note", type="note", icon="information")
    render_notes(f, usage_notes(g, c), "Usage note", type="note", icon="puzzle")
    render_notes(f, change_notes(g, c), "Change note", type="caution", icon="warning")
    render_notes(f, examples(g, c), "Example", type="note", icon="open-book")

def write_index_mdx(dir_path, top, g):
    top_not = notation(g, top)
    top_label = label(g, top)
    top_def = definition(g, top)
    mdx_path = os.path.join(dir_path, "index.mdx")
    with open(mdx_path, "w", encoding="utf-8") as f:
        # Frontmatter
        f.write(f"---\ntitle: {top_label}\ndescription: {top_def}\nlabel: {top_not}\n---\n\n")
        f.write("import { Tabs, TabItem, LinkButton, Aside } from '@astrojs/starlight/components';\n\n")
        f.write(f"{top_def}\n\n")
        render_all_notes(f, g, top)
        # Secondary classes
        for sec in get_narrower(g, top):
            sec_not = notation(g, sec)
            sec_label = label(g, sec)
            sec_def = definition(g, sec)
            f.write(f"## {sec_not} {sec_label}\n\n")
            f.write(f"{sec_def}\n\n")
            render_all_notes(f, g, sec)
            tertiaries = get_narrower(g, sec)
            tertiaries = get_narrower(g, sec)
            if tertiaries:
                f.write("<Tabs>\n\n")
                for tert in tertiaries:
                    tert_not = notation(g, tert)
                    tert_label = label(g, tert)
                    tert_def = definition(g, tert)
                    f.write(f'  <TabItem label="{tert_not} {tert_label}">\n')
                    f.write(f"    {tert_def}\n")
                    render_all_notes(f, g, tert)
                    f.write("  </TabItem>\n\n")
                f.write("</Tabs>\n\n")

def main():
    if len(sys.argv) != 4:
        print("Usage: export_outline_mdx.py INPUT.ttl SCHEME_IRI OUTDIR", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

    g = Graph()
    g.parse(in_ttl, format="turtle")

    # Expand CURIE using graph's namespace bindings
    scheme = URIRef(scheme_iri)
    if ":" in scheme_iri and not scheme_iri.startswith("http"):
        prefix, local = scheme_iri.split(":", 1)
        for p, n in g.namespaces():
            if p == prefix:
                scheme = URIRef(str(n) + local)
                break

    # Find all top concepts for the scheme
    top_concepts = get_top_concepts(g, scheme)

    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    for top in top_concepts:
        top_not = notation(g, top)
        dir_path = os.path.join(out_dir, top_not)
        os.makedirs(dir_path, exist_ok=True)
        write_index_mdx(dir_path, top, g)
        print(f"Wrote {os.path.join(dir_path, 'index.mdx')}", file=sys.stderr)

if __name__ == "__main__":
    main()