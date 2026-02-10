#!/usr/bin/env python3
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from collections import defaultdict
import sys

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def get_lang_pref(g, s, p, lang="en"):
    vals = list(g.objects(s, p))
    # prefer requested language
    for v in vals:
        if getattr(v, "language", None) == lang:
            return str(v)
    # fallback: any
    return str(vals[0]) if vals else None

def get_lang_all(g, s, p, lang="en"):
    out = []
    for v in g.objects(s, p):
        if getattr(v, "language", None) == lang:
            out.append(str(v))
    # if none in lang, fall back to untagged/other lang
    if not out:
        out = [str(v) for v in g.objects(s, p)]
    return out

def notation(g, c):
    n = next(g.objects(c, SKOS.notation), None)
    return str(n) if n else ""

def code_key(code: str):
    # numeric-aware key for dotted codes like 1.2.10
    try:
        return [int(x) for x in code.split(".")]
    except Exception:
        return [code]

def md_escape(s: str) -> str:
    # minimal escaping for markdown
    return s.replace("\r\n", "\n").replace("\r", "\n")

def indent_lines(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line.strip() != "" else prefix.rstrip() for line in text.split("\n"))

def main():
    if len(sys.argv) < 4:
        print("Usage: export_outline_md.py INPUT.ttl SCHEME_IRI OUTPUT.md", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, out_md = sys.argv[1], sys.argv[2], sys.argv[3]
    scheme = URIRef(scheme_iri)

    g = Graph()
    g.parse(in_ttl, format="turtle")

    # collect concepts in scheme
    concepts = {c for c in g.subjects(RDF.type, SKOS.Concept) if (c, SKOS.inScheme, scheme) in g}
    if not concepts:
        raise SystemExit(f"No skos:Concept with skos:inScheme {scheme_iri} found in {in_ttl}")

    # top concepts from scheme
    tops = [c for c in g.objects(scheme, SKOS.hasTopConcept) if c in concepts]
    if not tops:
        raise SystemExit(f"No skos:hasTopConcept found for scheme {scheme_iri} (or not inScheme)")

    # build children map from skos:broader
    children = defaultdict(list)
    broader_count = defaultdict(int)

    for child in concepts:
        for parent in g.objects(child, SKOS.broader):
            if parent in concepts:
                children[parent].append(child)
                broader_count[child] += 1

    # sort children and tops by notation
    def sort_nodes(nodes):
        return sorted(nodes, key=lambda c: (code_key(notation(g, c)), (get_lang_pref(g, c, SKOS.prefLabel) or "").lower()))

    tops = sort_nodes(tops)
    for p in list(children.keys()):
        children[p] = sort_nodes(children[p])

    lines = []
    lines.append(f"# NZLUM outline ({scheme_iri})")
    lines.append("")

    def emit(concept, depth):
        code = notation(g, concept)
        lab = get_lang_pref(g, concept, SKOS.prefLabel) or str(concept)
        defi = get_lang_pref(g, concept, SKOS.definition) or ""

        ind = "  " * depth  # indentation for nested list
        # Enumerated list item: use code as the visible "numbering"
        lines.append(f"{ind}- **{code} {md_escape(lab)}**")
        if defi:
            lines.append(f"{ind}  {md_escape(defi)}")

        scope_notes = get_lang_all(g, concept, SKOS.scopeNote)
        for i, sn in enumerate(scope_notes):
            sn = md_escape(sn)
            lines.append(f"{ind}  > [!NOTE]")
            lines.append(f"{ind}  > {sn}")
            # blank line between multiple NOTE blocks
            if i != len(scope_notes) - 1:
                lines.append(f"{ind}  ")

        usage_notes = get_lang_all(g, concept, SKOS.usageNote)

        # blank line between NOTE section and TIP section
        if scope_notes and usage_notes:
            lines.append(f"{ind}  ")

        for j, un in enumerate(usage_notes):
            un = md_escape(un)
            lines.append(f"{ind}  > [!TIP]")
            lines.append(f"{ind}  > {un}")
            if j != len(usage_notes) - 1:
                lines.append(f"{ind}  ")


        # blank line between items at same depth improves readability in GitHub
        lines.append("")

        for ch in children.get(concept, []):
            emit(ch, depth + 1)

    for t in tops:
        emit(t, 0)

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    print(f"Wrote {out_md}", file=sys.stderr)

if __name__ == "__main__":
    main()
