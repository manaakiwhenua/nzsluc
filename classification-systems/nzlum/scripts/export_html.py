#!/usr/bin/env python3
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL, DCTERMS, FOAF
from collections import defaultdict
import html as htmllib
import sys

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
LU = Namespace("https://nzlum.landcareresearch.co.nz/landuse/")
ADMS = Namespace("http://www.w3.org/ns/adms#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")


def get_en(g, s, p):
    for o in g.objects(s, p):
        if getattr(o, "language", None) == "en":
            return str(o)
    o = next(g.objects(s, p), None)
    return str(o) if o else None


def get_all_lang(g, s, p, lang="en"):
    out = [str(v) for v in g.objects(s, p) if getattr(v, "language", None) == lang]
    if not out:
        out = [str(v) for v in g.objects(s, p)]
    return out


def get_change_notes(g, s):
    # skos:changeNote is used with both plain-text literals and GitHub issue
    # URIs in this vocabulary; keep both, tagging URIs so callers can render
    # them as links instead of escaping them as text.
    notes = []
    for v in g.objects(s, SKOS.changeNote):
        if isinstance(v, URIRef):
            notes.append(("uri", str(v)))
        else:
            notes.append(("text", str(v)))
    return notes


def notation(g, c):
    n = next(g.objects(c, SKOS.notation), None)
    return str(n) if n else ""


def label(g, c):
    return get_en(g, c, SKOS.prefLabel) or str(c)


def colour(g, c):
    n = next(g.objects(c, LU.colour), None)
    return str(n) if n else ""


def code_key(code: str):
    try:
        return [int(x) for x in code.split(".")]
    except Exception:
        return [code]


def esc(s):
    return htmllib.escape(s or "", quote=True)


def contrast_text(hex_colour: str) -> str:
    # simple relative-luminance check so swatch text stays legible
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        return "#000000"
    r, g_, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g_ + 0.114 * b) / 255
    return "#000000" if luminance > 0.6 else "#ffffff"


def def_link(code: str, text: str) -> str:
    if not code:
        return esc(text)
    return f'<a class="def-link" href="#def-{esc(code)}">{esc(text)}</a>'


def swatch_td(hex_colour: str, rowspan: int) -> str:
    if not hex_colour:
        return f'<td class="colour" rowspan="{rowspan}"></td>'
    fg = contrast_text(hex_colour)
    return (
        f'<td class="colour" rowspan="{rowspan}" '
        f'style="background:{esc(hex_colour)};color:{fg};">{esc(hex_colour)}</td>'
    )


def swatch_span(hex_colour: str) -> str:
    if not hex_colour:
        return ""
    fg = contrast_text(hex_colour)
    return f' <span class="swatch" style="background:{esc(hex_colour)};color:{fg};">{esc(hex_colour)}</span>'


def scheme_metadata(g, scheme):
    root = next(g.objects(scheme, DCTERMS.isVersionOf), scheme)
    scheme_title = get_en(g, root, DCTERMS.title) or get_en(g, scheme, DCTERMS.title)
    version = next(g.objects(scheme, OWL.versionInfo), None)
    issued = next(g.objects(scheme, DCTERMS.issued), None)
    status_node = next(g.objects(scheme, ADMS.status), None)
    status_label = get_en(g, status_node, RDFS.label) if status_node else None
    homepage = next(g.objects(scheme, FOAF.homepage), None) or next(g.objects(root, FOAF.homepage), None)

    def split_camel_label(local_name):
        words, current = [], ""
        for ch in local_name:
            if ch.isupper() and current:
                words.append(current)
                current = ch
            else:
                current += ch
        if current:
            words.append(current)
        if not words:
            return None
        return " ".join([words[0]] + [w.lower() for w in words[1:]])

    def repo_info(node):
        repo = next(g.objects(node, DOAP.repository), None)
        if repo is None:
            return None, None
        browse = next(g.objects(repo, DOAP.browse), None)
        rtype = next(g.objects(repo, RDF.type), None)
        label = split_camel_label(rtype.split("#")[-1]) if rtype else None
        return browse, (label or "Repository")

    repository, repository_label = repo_info(scheme)
    if repository is None:
        repository, repository_label = repo_info(root)

    def version_ref(node):
        if node is None:
            return None
        v = next(g.objects(node, OWL.versionInfo), None)
        return {"iri": str(node), "version": str(v) if v else str(node)}

    superseded_by = version_ref(next(g.objects(scheme, DCTERMS.isReplacedBy), None))
    replaces = version_ref(next(g.objects(scheme, DCTERMS.replaces), None))

    relations = []
    relation_sources = [scheme] if root == scheme else [scheme, root]
    seen_rels = set()
    for src in relation_sources:
        for rel in g.objects(src, DCTERMS.relation):
            if rel in seen_rels:
                continue
            seen_rels.add(rel)
            descs = defaultdict(list)
            for d in g.objects(rel, DCTERMS.description):
                lang = getattr(d, "language", None) or "en"
                descs[lang].append(str(d))
            creator_names = []
            for creator in g.objects(rel, DCTERMS.creator):
                creator_names.extend(str(nm) for nm in g.objects(creator, FOAF.name))
            relations.append((descs, creator_names))

    return {
        "title": scheme_title,
        "version": str(version) if version else None,
        "issued": str(issued) if issued else None,
        "status": status_label,
        "homepage": str(homepage) if homepage else None,
        "repository": str(repository) if repository else None,
        "repository_label": repository_label,
        "superseded_by": superseded_by,
        "replaces": replaces,
        "relations": relations,
    }


def render_relation_block(descs, creator_names) -> str:
    parts = ['<div class="whakatauki">']
    if "mi" in descs:
        for t in descs["mi"]:
            parts.append(f'<p class="mi" lang="mi">“{esc(t)}”</p>')
    for lang, texts in descs.items():
        if lang == "mi":
            continue
        for t in texts:
            parts.append(f'<p class="translation">“{esc(t)}”</p>')
    if creator_names:
        attributed = min(creator_names, key=len)
        parts.append(f'<p class="attribution">— {esc(attributed)}</p>')
    parts.append("</div>")
    return "\n".join(parts)


def render_change_note(kind, value):
    if kind != "uri":
        return esc(value)
    return f'<a href="{esc(value)}">{esc(value)}</a>'


def note_boxes(notes):
    out = []
    for sn in notes["scope_notes"]:
        out.append(f'<div class="callout note"><span class="callout-label">Scope note</span> {esc(sn)}</div>')
    for un in notes["usage_notes"]:
        out.append(f'<div class="callout tip"><span class="callout-label">Usage note</span> {esc(un)}</div>')
    for ex in notes["examples"]:
        out.append(f'<div class="callout example"><span class="callout-label">Example</span> {esc(ex)}</div>')
    for kind, cn in notes["change_notes"]:
        out.append(f'<div class="callout changed"><span class="callout-label">Change note</span> {render_change_note(kind, cn)}</div>')
    for hn in notes["historical_notes"]:
        out.append(f'<div class="callout history"><span class="callout-label">Historical note</span> {esc(hn)}</div>')
    return out


def concept_notes(g, concept):
    return {
        "definition": get_en(g, concept, SKOS.definition),
        "scope_notes": get_all_lang(g, concept, SKOS.scopeNote),
        "usage_notes": get_all_lang(g, concept, SKOS.usageNote),
        "examples": get_all_lang(g, concept, SKOS.example),
        "change_notes": get_change_notes(g, concept),
        "historical_notes": get_all_lang(g, concept, SKOS.historicalNote),
        "sources": get_all_lang(g, concept, DCTERMS.source),
    }


def render_concept_heading(g, concept, tag, extra_class=""):
    code, lab, col = notation(g, concept), label(g, concept), colour(g, concept)
    notes = concept_notes(g, concept)
    cls = f' class="{extra_class}"' if extra_class else ""
    html = [f'<{tag}{cls} id="def-{esc(code)}"><span class="code">{esc(code)}</span> {esc(lab)}{swatch_span(col)}</{tag}>']
    if notes["definition"]:
        html.append(f'<p class="definition">{esc(notes["definition"])}</p>')
    for src in notes["sources"]:
        html.append(f'<p class="source">Source: {esc(src)}</p>')
    html.extend(note_boxes(notes))
    return "\n".join(html)


def render_tertiary_item(g, concept):
    code, lab, col = notation(g, concept), label(g, concept), colour(g, concept)
    notes = concept_notes(g, concept)
    parts = [f'<div class="tertiary-item" id="def-{esc(code)}">']
    parts.append(f'<p class="tertiary-head"><span class="code">{esc(code)}</span> <strong>{esc(lab)}</strong>{swatch_span(col)}</p>')
    if notes["definition"]:
        parts.append(f'<p class="definition">{esc(notes["definition"])}</p>')
    for src in notes["sources"]:
        parts.append(f'<p class="source">Source: {esc(src)}</p>')
    parts.extend(note_boxes(notes))
    parts.append("</div>")
    return "\n".join(parts)


def render_definitions(g, tops, children):
    sections = ['<section class="definitions"><h2 class="definitions-title">Class definitions</h2>']
    for t, top in enumerate(tops):
        top_class = "first-primary" if t == 0 else ""
        sections.append(render_concept_heading(g, top, "h2", top_class))
        for i, sec in enumerate(children.get(top, [])):
            sec_class = "first-secondary" if i == 0 else ""
            sections.append(render_concept_heading(g, sec, "h3", sec_class))
            ters = children.get(sec, [])
            if ters:
                items = [render_tertiary_item(g, t) for t in ters]
                sections.append('<div class="tertiary-group">' + "".join(items) + "</div>")
    sections.append("</section>")
    return "\n".join(sections)


def main():
    if len(sys.argv) < 5:
        print("Usage: export_html.py INPUT.ttl SCHEME_IRI OUT.html TITLE", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, out_html, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    scheme = URIRef(scheme_iri)

    g = Graph()
    g.parse(in_ttl, format="turtle")

    concepts = {c for c in g.subjects(RDF.type, SKOS.Concept) if (c, SKOS.inScheme, scheme) in g}

    tops = [c for c in g.objects(scheme, SKOS.hasTopConcept) if c in concepts]
    if not tops:
        raise SystemExit(f"No skos:hasTopConcept found for scheme {scheme_iri} (or top concepts not inScheme).")

    children = defaultdict(list)
    broader = defaultdict(list)

    for c in concepts:
        for p in g.objects(c, SKOS.broader):
            if p in concepts:
                broader[c].append(p)
                children[p].append(c)

    poly = [c for c, ps in broader.items() if len(ps) > 1]
    if poly:
        print(f"WARNING: {len(poly)} concepts have multiple skos:broader parents; table will pick the first (arbitrary).", file=sys.stderr)

    def sort_nodes(nodes):
        return sorted(nodes, key=lambda c: (code_key(notation(g, c)), label(g, c).lower()))

    tops = sort_nodes(tops)
    for p in list(children.keys()):
        children[p] = sort_nodes(children[p])

    # rows: (top_code, top_label, top_colour, sec_code, sec_label, sec_colour, ter_code, ter_label, ter_colour)
    rows = []
    for top in tops:
        top_code, top_label, top_colour = notation(g, top), label(g, top), colour(g, top)

        secs = children.get(top, [])
        if not secs:
            rows.append((top_code, top_label, top_colour, "", "", "", "", "", ""))
            continue

        for sec in secs:
            sec_code, sec_label, sec_colour = notation(g, sec), label(g, sec), colour(g, sec)

            ters = children.get(sec, [])
            if not ters:
                rows.append((top_code, top_label, top_colour, sec_code, sec_label, sec_colour, "", "", ""))
                continue

            for ter in ters:
                ter_code, ter_label, ter_colour = notation(g, ter), label(g, ter), colour(g, ter)
                rows.append((top_code, top_label, top_colour, sec_code, sec_label, sec_colour, ter_code, ter_label, ter_colour))

    # precompute rowspans for primary/secondary groups, mirroring the merge
    # logic used for the xlsx export (contiguous runs of identical values).
    n = len(rows)
    primary_span = [0] * n
    secondary_span = [0] * n
    skip_primary = [False] * n
    skip_secondary = [False] * n

    i = 0
    while i < n:
        j = i
        while j + 1 < n and rows[j + 1][0:2] == rows[i][0:2]:
            j += 1
        primary_span[i] = j - i + 1
        for k in range(i + 1, j + 1):
            skip_primary[k] = True
        i = j + 1

    i = 0
    while i < n:
        j = i
        while (j + 1 < n and rows[j + 1][0:2] == rows[i][0:2] and rows[j + 1][3:5] == rows[i][3:5]):
            j += 1
        secondary_span[i] = j - i + 1
        for k in range(i + 1, j + 1):
            skip_secondary[k] = True
        i = j + 1

    body_rows = []
    for idx, (p_code, p_lab, p_col, s_code, s_lab, s_col, t_code, t_lab, t_col) in enumerate(rows):
        cells = []
        if not skip_primary[idx]:
            span = primary_span[idx]
            cells.append(f'<td class="code" rowspan="{span}">{esc(p_code)}</td>')
            cells.append(f'<td class="label primary" rowspan="{span}">{def_link(p_code, p_lab)}</td>')
            cells.append(swatch_td(p_col, span))
        if s_code == "" and s_lab == "":
            if not skip_primary[idx]:
                span = primary_span[idx]
                cells.append(f'<td class="code" rowspan="{span}"></td>')
                cells.append(f'<td class="label secondary" rowspan="{span}"></td>')
                cells.append(swatch_td("", span))
        elif not skip_secondary[idx]:
            span = secondary_span[idx]
            cells.append(f'<td class="code" rowspan="{span}">{esc(s_code)}</td>')
            cells.append(f'<td class="label secondary" rowspan="{span}">{def_link(s_code, s_lab)}</td>')
            cells.append(swatch_td(s_col, span))

        cells.append(f'<td class="code">{esc(t_code)}</td>')
        cells.append(f'<td class="label tertiary">{def_link(t_code, t_lab)}</td>')
        cells.append(swatch_td(t_col, 1))

        row_class = ' class="new-primary"' if not skip_primary[idx] else ""
        body_rows.append(f"<tr{row_class}>" + "".join(cells) + "</tr>")

    meta = scheme_metadata(g, scheme)
    definitions_html = render_definitions(g, tops, children)

    meta_fields = []
    if meta["status"]:
        meta_fields.append(("Status", esc(meta["status"])))
    if meta["issued"]:
        meta_fields.append(("Issued", esc(meta["issued"])))
    if meta["homepage"]:
        meta_fields.append(("Website", f'<a href="{esc(meta["homepage"])}">{esc(meta["homepage"])}</a>'))
    if meta["repository"]:
        meta_fields.append((meta["repository_label"], f'<a href="{esc(meta["repository"])}">{esc(meta["repository"])}</a>'))
    if meta["replaces"]:
        r = meta["replaces"]
        meta_fields.append(("Replaces", f'<a href="{esc(r["iri"])}">NZLUM v{esc(r["version"])}</a>'))
    if meta["superseded_by"]:
        s = meta["superseded_by"]
        meta_fields.append(("Superseded by", f'<a href="{esc(s["iri"])}">NZLUM v{esc(s["version"])}</a>'))
    meta_fields.append(("Scheme IRI", esc(scheme_iri)))
    meta_fields_html = "".join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in meta_fields)

    relations_html = "".join(render_relation_block(descs, names) for descs, names in meta["relations"])

    superseded_notice_html = ""
    if meta["superseded_by"]:
        s = meta["superseded_by"]
        superseded_notice_html = (
            '<div class="notice superseded">'
            f'&#9888; This version has been <strong>superseded</strong> by '
            f'<a href="{esc(s["iri"])}">NZLUM v{esc(s["version"])}</a>.'
            "</div>"
        )

    heading_title = meta["title"] or title
    version_badge = f' <span class="version">v{esc(meta["version"])}</span>' if meta["version"] else ""
    title_html = (
        f'<a class="title-link" href="{esc(meta["homepage"])}">{esc(heading_title)}</a>'
        if meta["homepage"] else esc(heading_title)
    )

    footer_title = f'{esc(heading_title)}{" v" + esc(meta["version"]) if meta["version"] else ""}'
    footer_left_html = (
        f'<a href="{esc(meta["homepage"])}">{footer_title}</a>' if meta["homepage"] else footer_title
    )

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 12mm 10mm 16mm 10mm;
    font-family: "Helvetica Neue", Arial, sans-serif;
    @bottom-left {{ content: element(footer-left); color: #555; }}
    @bottom-center {{ content: element(footer-center); color: #555; }}
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 7.5pt;
      font-family: "Helvetica Neue", Arial, sans-serif;
      color: #555;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    color: #1a1a1a;
    margin: 0;
  }}
  .footer-left {{ position: running(footer-left); font-size: 7.5pt; }}
  .footer-center {{ position: running(footer-center); font-size: 7.5pt; }}
  .footer-left a, .footer-center a {{
    color: #555;
    text-decoration: none;
    border-bottom: 0.75pt dotted #999;
  }}
  @media screen {{
    .footer-left, .footer-center {{ display: none; }}
  }}
  h1 {{ font-size: 18pt; margin: 0 0 3mm 0; }}
  a.title-link {{ color: inherit; text-decoration: none; border-bottom: 1pt dotted #999; }}
  .version {{ font-weight: 400; color: #666; font-size: 12pt; }}
  .scheme-meta {{ margin-bottom: 6mm; }}
  dl.meta-fields {{
    margin: 2mm 0 0 0;
    font-size: 9pt;
  }}
  dl.meta-fields div {{
    display: inline-block;
    white-space: nowrap;
    margin: 0 8mm 2mm 0;
  }}
  dl.meta-fields dt {{ display: inline; font-weight: 700; color: #444; margin-right: 2mm; }}
  dl.meta-fields dd {{ display: inline; margin: 0; color: #555; }}
  .notice.superseded {{
    margin-top: 4mm;
    padding: 2.5mm 5mm;
    border-left: 3pt solid #b45309;
    background: #fffbeb;
    color: #7c2d12;
    font-size: 9.5pt;
    max-width: 160mm;
  }}
  .notice.superseded a {{ color: inherit; font-weight: 700; }}
  .whakatauki {{
    margin-top: 4mm;
    padding: 3mm 5mm;
    border-left: 3pt solid #888;
    background: #f7f7f7;
    max-width: 160mm;
  }}
  .whakatauki p {{ margin: 0 0 1mm 0; font-size: 9.5pt; }}
  .whakatauki .mi, .whakatauki .translation {{ font-style: italic; font-weight: 600; color: #333; }}
  .whakatauki .attribution {{ font-size: 8.5pt; color: #666; text-align: right; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 8.5pt;
  }}
  thead th {{
    background: #2d2d2d;
    color: #fff;
    text-align: left;
    padding: 3px 5px;
  }}
  td {{
    border: 0.5pt solid #bbb;
    padding: 2.5px 5px;
    vertical-align: top;
  }}
  td.code {{ white-space: nowrap; text-align: right; font-variant-numeric: tabular-nums; }}
  td.colour {{ text-align: center; font-family: monospace; font-size: 7.5pt; white-space: nowrap; }}
  tr.new-primary {{ border-top: 1.5pt solid #333; }}
  td.label.primary {{ font-weight: 700; }}
  td.label.secondary {{ font-weight: 600; }}
  a.def-link {{
    color: inherit;
    text-decoration: none;
    border-bottom: 0.75pt dotted #888;
  }}
  thead {{ display: table-header-group; }}
  tr {{ page-break-inside: avoid; }}

  section.definitions {{ margin-top: 8mm; page-break-before: always; }}
  h2.definitions-title {{ font-size: 15pt; }}
  section.definitions h2:not(.definitions-title) {{
    font-size: 14pt;
    border-bottom: 1.5pt solid #333;
    padding-bottom: 1.5mm;
    margin-top: 8mm;
    page-break-before: always;
  }}
  section.definitions h2.first-primary {{ page-break-before: avoid; margin-top: 4mm; }}
  section.definitions h3 {{ font-size: 11.5pt; margin-top: 5mm; color: #222; page-break-before: always; }}
  section.definitions h3.first-secondary {{ page-break-before: avoid; margin-top: 0; }}
  section.definitions .code {{
    font-family: monospace;
    color: #666;
    margin-right: 2mm;
    font-size: 0.9em;
  }}
  .swatch {{
    display: inline-block;
    padding: 0 4px;
    border-radius: 2px;
    font-family: monospace;
    font-size: 7.5pt;
    margin-left: 5px;
  }}
  p.definition {{ margin: 1mm 0 1mm 0; font-size: 9pt; }}
  p.source {{ margin: 0 0 1mm 0; font-size: 8pt; font-style: italic; color: #666; }}
  .tertiary-group {{
    columns: 2;
    column-gap: 8mm;
    margin-top: 2mm;
  }}
  .tertiary-item {{
    break-inside: avoid;
    margin-bottom: 3mm;
    padding-bottom: 2mm;
    border-bottom: 0.5pt solid #ddd;
  }}
  p.tertiary-head {{ margin: 0 0 1mm 0; font-size: 9.5pt; }}
  .callout {{
    font-size: 8pt;
    padding: 1.5px 6px;
    border-left: 2.5pt solid;
    margin: 1.5mm 0;
    break-inside: avoid;
  }}
  .callout-label {{ font-weight: 700; margin-right: 3px; }}
  .callout.note {{ border-color: #3b82f6; background: #eff6ff; }}
  .callout.tip {{ border-color: #16a34a; background: #f0fdf4; }}
  .callout.example {{ border-color: #d97706; background: #fffbeb; }}
  .callout.changed {{ border-color: #7c3aed; background: #f5f3ff; }}
  .callout.changed a {{ color: inherit; }}
  .callout.history {{ border-color: #64748b; background: #f8fafc; }}
</style>
</head>
<body>
<div id="footer-left" class="footer-left">{footer_left_html}</div>
<div id="footer-center" class="footer-center"><a href="#class-table">&uarr; Back to table</a></div>
<div class="scheme-meta">
  <h1>{title_html}{version_badge}</h1>
  <dl class="meta-fields">{meta_fields_html}</dl>
  {superseded_notice_html}
  {relations_html}
</div>
<table id="class-table">
<thead>
<tr>
<th>Primary code</th><th>Primary class</th><th>Primary colour</th>
<th>Secondary code</th><th>Secondary class</th><th>Secondary colour</th>
<th>Tertiary code</th><th>Tertiary class</th><th>Tertiary colour</th>
</tr>
</thead>
<tbody>
{chr(10).join(body_rows)}
</tbody>
</table>
{definitions_html}
</body>
</html>
"""

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"Wrote {out_html}", file=sys.stderr)


if __name__ == "__main__":
    main()
