#!/usr/bin/env python3
"""Export dereferenceable Linked Data documents for every NZLUM resource.

For every URI minted under BASE (default https://nzlum.landcareresearch.co.nz/landuse/)
this writes four sibling documents under OUT, mirroring the URI path:

    <OUT>/landuse/concept/conservation.html     human-readable landing page
    <OUT>/landuse/concept/conservation.ttl      Turtle
    <OUT>/landuse/concept/conservation.jsonld   JSON-LD
    <OUT>/landuse/concept/conservation.rdf      RDF/XML

The tree is laid out so it can be dropped into the public/ folder of the nzlum-site
Astro project. GitHub Pages serves "foo.html" for a request to "/foo" without a
redirect, so the concept URI itself resolves to the HTML page, which advertises the
RDF serialisations with <link rel="alternate"> and embeds JSON-LD. There is no
content negotiation on GitHub Pages; this is the static (tier 1) publication.

It also writes:

    <OUT>/landuse/index.html                    index of everything in the namespace
    <OUT>/landuse/all.{ttl,jsonld,rdf}          the whole served graph
    <OUT>/landuse/code/nzlum0.4.0/2.8.2.html    lookup of a code *within a version*,
                                                redirecting to the concept URI
    <OUT>/landuse/code/nzlum0.4.0/index.html    code table for that version
    <OUT>/landuse/code/index.html               list of versions

Concept URIs are unversioned. The served description of a concept is taken from the
latest NZLUM version it appears in; it is marked as being in every version's scheme
that includes it. A concept that was dropped in a later version is served from the
last version that contained it, with owl:deprecated true and a skos:historyNote added.
"""
import argparse
import html
import json
import os
import re
import sys
from collections import defaultdict

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, FOAF, OWL, RDF, RDFS, XSD

# Plain namespace: the vocabulary also uses non-standard terms such as skos:usageNote.
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")

FORMATS = [
    ("ttl", "text/turtle", "turtle", "Turtle"),
    ("jsonld", "application/ld+json", "json-ld", "JSON-LD"),
    ("rdf", "application/rdf+xml", "pretty-xml", "RDF/XML"),
]

LABEL_PREDS = [SKOS.prefLabel, RDFS.label, DCTERMS.title, FOAF.name]
NOTE_PREDS = [
    (SKOS.definition, "Definition"),
    (SKOS.scopeNote, "Scope note"),
    (SKOS.usageNote, "Usage note"),
    (SKOS.example, "Example"),
    (SKOS.historyNote, "History note"),
    (SKOS.editorialNote, "Editorial note"),
    (SKOS.changeNote, "Change note"),
    (DCTERMS.source, "Source"),
    (DCTERMS.description, "Description"),
    (RDFS.comment, "Comment"),
]
# Predicates rendered in dedicated sections, so they are left out of the generic table.
HANDLED = set(p for p, _ in NOTE_PREDS) | set(LABEL_PREDS) | {
    RDF.type, SKOS.notation, SKOS.broader, SKOS.narrower, SKOS.inScheme,
    SKOS.topConceptOf, SKOS.hasTopConcept, SKOS.member, OWL.deprecated,
}


# --------------------------------------------------------------------------- helpers

def parse_version(v):
    return tuple(int(x) for x in v.split("."))


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(text):
    """Approximates github-slugger, which Starlight uses for heading anchors."""
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = s.replace(" ", "-")
    return s


def notation_key(n):
    parts = re.split(r"[.\s]+", str(n or ""))
    key = []
    for p in parts:
        key.append((0, int(p)) if p.isdigit() else (1, p))
    return key


def lits(g, s, p, lang_first="en"):
    """All literal values of (s, p), English first, then other languages, then plain."""
    vals = [o for o in g.objects(s, p)]
    def k(o):
        lang = getattr(o, "language", None)
        return (0 if lang == lang_first else 1 if lang else 2, str(o))
    return sorted(vals, key=k)


def first_lit(g, s, p):
    v = lits(g, s, p)
    return str(v[0]) if v else None


def label_of(g, r, base):
    for p in LABEL_PREDS:
        v = first_lit(g, r, p)
        if v:
            return v
    n = first_lit(g, r, SKOS.notation)
    if n:
        return n
    # a versioned scheme without its own title: "<parent title> v<version>"
    parent = next(g.objects(r, DCTERMS.isVersionOf), None)
    ver = first_lit(g, r, OWL.versionInfo)
    if parent is not None and ver:
        t = first_lit(g, parent, DCTERMS.title)
        if t:
            return f"{t} v{ver}"
    s = str(r)
    return s[len(base):] if s.startswith(base) else s


def types_of(g, r):
    return sorted(set(g.objects(r, RDF.type)), key=str)


def is_a(g, r, t):
    return (r, RDF.type, t) in g


def rel_path(uri, base):
    return str(uri)[len(base):]


def copy_bindings(dst, *srcs):
    for g in srcs:
        for prefix, ns in g.namespaces():
            if prefix and prefix not in ("", "default"):
                dst.bind(prefix, ns, override=False, replace=False)


def new_graph(bind="core"):
    """A Graph with only the given default bindings; older rdflib lacks the argument."""
    try:
        return Graph(bind_namespaces=bind)
    except TypeError:
        return Graph()


def prune_jsonld_context(text):
    """Drop @context prefixes that nothing in the document uses (older rdflib adds many defaults)."""
    doc = json.loads(text)
    ctx = doc.get("@context")
    if not isinstance(ctx, dict):
        return text
    body = json.dumps({k: v for k, v in doc.items() if k != "@context"})
    keep = {}
    for prefix, val in ctx.items():
        if not isinstance(val, str) or not prefix or prefix.startswith("@"):
            keep[prefix] = val
        elif f'"{prefix}:' in body:
            keep[prefix] = val
    doc["@context"] = keep
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def writefile(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------- RDF side

class Exporter:
    def __init__(self, out, base, site, versions, term_lists):
        self.out = out
        self.base = base.rstrip("/") + "/"
        self.site = site.rstrip("/")
        self.versions = sorted(versions, key=parse_version)        # ascending
        self.latest = self.versions[-1]
        self.vgraphs = {}
        for v in self.versions:
            g = new_graph("none")
            g.parse(versions[v])
            self.vgraphs[v] = g
        self.tgraphs = {}                                           # scheme URI -> Graph
        for path in term_lists:
            g = new_graph("none")
            g.parse(path)
            schemes = list(g.subjects(RDF.type, SKOS.ConceptScheme))
            if len(schemes) != 1:
                sys.exit(f"{path}: expected exactly one skos:ConceptScheme, found {len(schemes)}")
            self.tgraphs[schemes[0]] = g
        self.G = new_graph("core")
        copy_bindings(self.G, *self.vgraphs.values(), *self.tgraphs.values())
        self.present = defaultdict(list)                            # concept -> [versions]
        self.build_served_graph()

    def scheme_uri(self, v):
        return URIRef(f"{self.base}scheme/nzlum{v}")

    def build_served_graph(self):
        G = self.G
        for t in self.vgraphs[self.latest]:
            G.add(t)
        for v in self.versions:
            for c in self.vgraphs[v].subjects(SKOS.inScheme, self.scheme_uri(v)):
                self.present[c].append(v)
        for c, vs in self.present.items():
            last = vs[-1]
            if last != self.latest:
                for t in self.vgraphs[last].triples((c, None, None)):
                    G.add(t)
                G.add((c, OWL.deprecated, Literal(True)))
                G.add((c, SKOS.historyNote, Literal(
                    f"Last included in NZLUM {last}; not carried into NZLUM {self.latest}.", lang="en")))
            for v in vs:
                G.add((c, SKOS.inScheme, self.scheme_uri(v)))
        for g in self.tgraphs.values():
            for t in g:
                G.add(t)

    # ---- which resources to export
    def resources(self):
        subs = {s for s in self.G.subjects() if isinstance(s, URIRef)
                and str(s).startswith(self.base) and str(s) != self.base}
        dangling = {o for o in self.G.objects() if isinstance(o, URIRef)
                    and str(o).startswith(self.base) and o not in subs and str(o) != self.base}
        for d in sorted(dangling, key=str):
            print(f"warning: {d} is referenced but has no description; no documents written", file=sys.stderr)
        bad = [s for s in subs if not re.fullmatch(r"[A-Za-z0-9_./-]+", rel_path(s, self.base))
               or rel_path(s, self.base).endswith("/")]
        for b in bad:
            print(f"warning: {b} has a path not suitable for a static file; skipped", file=sys.stderr)
        return sorted(subs - set(bad), key=str)

    # ---- the RDF document served for a resource
    def describe(self, r):
        G = self.G
        d = new_graph("core")
        copy_bindings(d, G)

        if r in self.tgraphs:                                       # term-list scheme: whole list
            for t in self.tgraphs[r]:
                d.add(t)
        elif r in (self.scheme_uri(v) for v in self.versions):      # versioned scheme: whole version
            v = [v for v in self.versions if self.scheme_uri(v) == r][0]
            for t in self.vgraphs[v]:
                d.add(t)
        else:
            seen = set()
            def add_subject(s):
                for t in G.triples((s, None, None)):
                    d.add(t)
                    if isinstance(t[2], BNode) and t[2] not in seen:
                        seen.add(t[2])
                        add_subject(t[2])
            add_subject(r)
            # inverse links: everything for small resources, structural ones for concepts
            if is_a(G, r, SKOS.Concept):
                inv = [SKOS.member, SKOS.hasTopConcept]
            else:
                inv = None
            for s, p in G.subject_predicates(r):
                if isinstance(s, BNode):
                    continue
                if inv is None or p in inv:
                    d.add((s, p, r))
            # one hop of labels so the document is readable on its own
            for o in set(d.objects()) | set(d.subjects()):
                if isinstance(o, URIRef) and o != r:
                    for p in LABEL_PREDS + [SKOS.notation]:
                        for t in G.triples((o, p, None)):
                            d.add(t)

        # document-level metadata (Cool URIs / vocabulary publishing recipe)
        page = URIRef(f"{r}.html")
        d.add((r, FOAF.isPrimaryTopicOf, page))
        d.add((page, RDF.type, FOAF.Document))
        d.add((page, DCTERMS.format, Literal("text/html")))
        for ext, mime, _, _ in FORMATS:
            fd = URIRef(f"{r}.{ext}")
            d.add((page, DCTERMS.hasFormat, fd))
            d.add((fd, RDF.type, FOAF.Document))
            d.add((fd, FOAF.primaryTopic, r))
            d.add((fd, DCTERMS.format, Literal(mime)))
        return d

    def write_rdf(self, path_noext, g):
        for ext, _, fmt, _ in FORMATS:
            if fmt == "json-ld":
                out = prune_jsonld_context(g.serialize(format=fmt, auto_compact=True))
            else:
                out = g.serialize(format=fmt)
            writefile(f"{path_noext}.{ext}", out)

    # ---- site links for a concept in a given version
    def site_page(self, v, c):
        g = self.vgraphs[v]
        maj, mnr = v.split(".")[:2]
        top = c
        guard = 0
        while True:
            b = next(g.objects(top, SKOS.broader), None)
            if b is None or guard > 10:
                break
            top, guard = b, guard + 1
        top_not = (first_lit(g, top, SKOS.notation) or "").replace(".", "")
        url = f"{self.site}/classification/v{maj}-{mnr}/classes/{top_not}/"
        # On the class pages only secondary classes are headings; tertiary classes sit in
        # tabs under their secondary, so link tertiaries to the secondary's anchor.
        sec = c
        while sec != top:
            b = next(g.objects(sec, SKOS.broader), None)
            if b is None or b == top:
                break
            sec = b
        if sec != top:
            url += "#" + slugify(f"{first_lit(g, sec, SKOS.notation)} {first_lit(g, sec, SKOS.prefLabel) or ''}")
        return url

    def version_differences(self, v, c):
        """Fields whose value in version v differs from the served (latest) description."""
        g, G = self.vgraphs[v], self.G
        diffs = []
        for p, name in [(SKOS.notation, "code"), (SKOS.prefLabel, "label"),
                        (SKOS.definition, "definition"), (SKOS.broader, "parent")]:
            a = set(g.objects(c, p))
            b = set(G.objects(c, p))
            if a != b:
                diffs.append(name)
        return diffs


# --------------------------------------------------------------------------- HTML side

CSS = """
:root{--fg:#1b1b1b;--bg:#fff;--muted:#5c5c5c;--line:#d9d9d9;--accent:#0b5d3b;--chip:#eef3f0;--card:#fafafa;--zebra:#f4f6f5;--warn:#fff4e5;--warnline:#e0a04f;
  --c-classes:#2f7d4f;--c-commodity:#c47f17;--c-mgmt:#3b6fb6;--c-water:#2a9db5;--c-other:#8a8a8a;--c-scheme:#6b4fa0;--c-collection:#b0541c}
@media (prefers-color-scheme:dark){:root{--fg:#e8e8e8;--bg:#161616;--muted:#a3a3a3;--line:#3a3a3a;--accent:#7fd1a6;--chip:#22302a;--card:#1d1d1d;--zebra:#1f2422;--warn:#3a2d16;--warnline:#9a6a1f;
  --c-classes:#5fbf85;--c-commodity:#e0a040;--c-mgmt:#6f9fe0;--c-water:#5cc3d8;--c-other:#9a9a9a;--c-scheme:#a98be0;--c-collection:#e08a55}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--fg);background:var(--bg)}
.wrap{max-width:62rem;margin:0 auto;padding:0 16px}main{padding:.5rem 0 4rem}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
header.site{background:var(--chip);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;gap:1.25rem;align-items:center;flex-wrap:wrap;padding-top:.55rem;padding-bottom:.55rem;font-size:.95rem}
header.site nav{display:flex;gap:1.1rem;flex-wrap:wrap}header.site nav a{color:var(--fg)}
h1{font-size:1.9rem;line-height:1.2;margin:.2rem 0 .4rem}
h2{font-size:1.2rem;margin:2rem 0 .6rem;border-bottom:1px solid var(--line);padding-bottom:.25rem}
.n{color:var(--muted);font-weight:400;font-size:.95rem}
.hero{margin:1.5rem 0 1rem;padding:.2rem 0 .2rem 1rem;border-left:.4rem solid var(--hero,var(--line))}
.uri{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9rem;word-break:break-all;color:var(--muted);margin:.3rem 0}
.chip{display:inline-block;padding:.05rem .55rem;border-radius:1rem;background:var(--chip);font-size:.85rem;margin:0 .4rem .3rem 0;border:1px solid transparent}
.chip.kind{border-color:var(--k,var(--line));color:var(--k,var(--fg))}
.chip.code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:600}
.sw{display:inline-block;width:.95em;height:.95em;border:1px solid var(--line);vertical-align:-.12em;margin-right:.3em;border-radius:.15em}
.banner{background:var(--warn);border:1px solid var(--warnline);padding:.6rem .9rem;border-radius:.4rem;margin:1rem 0}
dl{display:grid;grid-template-columns:max-content 1fr;gap:.35rem 1.2rem}dt{color:var(--muted)}dd{margin:0}
@media (max-width:600px){dl{grid-template-columns:1fr}dt{margin-top:.5rem}}
table{border-collapse:collapse;width:100%;font-size:.95rem}
th,td{text-align:left;vertical-align:top;padding:.4rem .6rem;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600;font-size:.85rem;text-transform:uppercase;letter-spacing:.03em}
tbody tr:nth-child(even),table tr:nth-child(even):not(:first-child){background:var(--zebra)}
ul.plain{list-style:none;padding:0;margin:0}ul.plain li{padding:.15rem 0}
ul.cols{columns:15rem;column-gap:1.75rem;padding:.2rem 0}ul.cols li{break-inside:avoid}
ul.plain ul.plain{margin-left:1rem;padding-left:.6rem;border-left:2px solid var(--line)}
blockquote{margin:.3rem 0 .8rem;padding:.2rem .9rem;border-left:3px solid var(--line)}
.lang{font-size:.75rem;color:var(--muted);margin-left:.3rem}
/* cards: one per top-level group on the index */
.card{border:1px solid var(--line);border-left:.45rem solid var(--c,var(--accent));border-radius:.6rem;padding:1rem 1.25rem 1.1rem;margin:1.4rem 0;background:var(--card)}
.card>h2{margin:0 0 .7rem;border:0;padding:0;font-size:1.35rem;display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap}
.card>h2 a{color:var(--c,var(--accent))}.card>p{margin:.2rem 0 .8rem}
.card-classes{--c:var(--c-classes)}.card-commodity{--c:var(--c-commodity)}.card-mgmt{--c:var(--c-mgmt)}
.card-water{--c:var(--c-water)}.card-other{--c:var(--c-other)}.card-schemes{--c:var(--c-scheme)}
/* collapsible groups */
details{margin:.35rem 0;border:1px solid var(--line);border-radius:.45rem;background:var(--bg)}
details>summary{list-style:none;cursor:pointer;display:flex;gap:.5rem;align-items:baseline;padding:.45rem .75rem;border-radius:.45rem;font-weight:600}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"";display:inline-block;width:.45rem;height:.45rem;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(-45deg);transition:transform .15s;flex:none;position:relative;top:-.15rem}
details[open]>summary::before{transform:rotate(45deg)}
details>summary:hover{background:var(--chip)}
details>ul,details>details,details>p{margin:.2rem .75rem .75rem .75rem}
details details{border:0;border-left:2px solid var(--line);border-radius:0;margin-left:1rem}
details details>summary{font-weight:500;padding:.3rem .6rem}
footer{margin-top:3rem;padding:1rem 0 2rem;border-top:1px solid var(--line);font-size:.9rem;color:var(--muted)}
"""


class HtmlWriter:
    def __init__(self, ex):
        self.ex = ex
        self.G = ex.G
        self.base = ex.base
        self.site = ex.site

    # ---- generic rendering
    def ref(self, r):
        """Link for a URI, labelled if we know a label."""
        G = self.G
        if isinstance(r, BNode):
            return "<em>(anonymous resource)</em>"
        s = str(r)
        if s.startswith(self.base):
            lbl = label_of(G, r, self.base)
            n = first_lit(G, r, SKOS.notation)
            prefix = f"<code>{esc(n)}</code> " if n and n != lbl and is_a(G, r, SKOS.Concept) else ""
            return f'{prefix}<a href="{esc(s)}">{esc(lbl)}</a>'
        return f'<a href="{esc(s)}" rel="external">{esc(self.curie(r))}</a>'

    def curie(self, r):
        try:
            q = self.G.namespace_manager.qname(r)
            return q if ":" in q else str(r)
        except Exception:
            return str(r)

    def lit(self, o):
        lang = getattr(o, "language", None)
        dt = getattr(o, "datatype", None)
        s = esc(o)
        if isinstance(o, URIRef):
            return self.ref(o)
        if lang and lang != "en":
            return f'{s}<span class="lang">@{esc(lang)}</span>'
        if dt and dt not in (XSD.string,):
            return f'{s}<span class="lang">{esc(self.curie(dt))}</span>'
        return s

    def local(self, url):
        """Root-relative form of a URL on the site, so pages work locally and in production."""
        url = str(url)
        return url[len(self.site):] if url.startswith(self.site + "/") else url

    def page(self, title, body, uri=None, jsonld=None, alternates=None, canonical=None, refresh=None):
        # Navigation links are root-relative; the canonical and alternate links in the
        # head stay absolute because they are identifiers, not navigation.
        body = body.replace(f'href="{self.site}/', 'href="/')
        head = [f"<title>{esc(title)} · NZLUM</title>",
                '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
                f'<link rel="stylesheet" href="{esc(self.local(self.base))}nzlum-ld.css">']
        if canonical:
            head.append(f'<link rel="canonical" href="{esc(canonical)}">')
        for href, mime, name in alternates or []:
            head.append(f'<link rel="alternate" type="{mime}" href="{esc(href)}" title="{esc(name)}">')
        if refresh:
            head.append(f'<meta http-equiv="refresh" content="0; url={esc(self.local(refresh))}">')
        if jsonld:
            head.append('<script type="application/ld+json">'
                        + jsonld.replace("</", "<\\/") + "</script>")
        nav = (f'<header class="site"><div class="wrap"><a href="/"><strong>NZLUM</strong></a>'
               f'<nav><a href="{self.local(self.base)}">Vocabulary index</a>'
               f'<a href="{self.local(self.base)}code/">Code lookup</a>'
               f'<a href="/classification/system">Classification</a></nav></div></header>')
        foot = ('<footer><div class="wrap">Manaaki Whenua – Landcare Research · '
                f'<a href="/">nzlum.landcareresearch.co.nz</a> · '
                'Source: <a href="https://github.com/manaakiwhenua/nzsluc">manaakiwhenua/nzsluc</a> · '
                'Licence: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></div></footer>')
        return ("<!doctype html>\n<html lang=\"en\">\n<head>\n" + "\n".join(head) +
                "\n</head>\n<body>\n" + nav + '<main><div class="wrap">' + body + "</div></main>" + foot + "\n</body>\n</html>\n")

    def alternates_for(self, r):
        return [(f"{r}.{ext}", mime, name) for ext, mime, _, name in FORMATS]

    def formats_section(self, r):
        items = "".join(f'<li><a href="{esc(f"{r}.{ext}")}" type="{mime}">{name}</a> '
                        f'<span class="uri">{mime}</span></li>' for ext, mime, _, name in FORMATS)
        return (f"<h2 id=\"formats\">Other formats</h2><ul class=\"plain\">{items}</ul>"
                "<p class=\"uri\">Append <code>.ttl</code>, <code>.jsonld</code> or <code>.rdf</code> "
                "to the URI. The URI itself returns this page.</p>")

    def notes(self, r):
        out = []
        for p, name in NOTE_PREDS:
            vals = lits(self.G, r, p)
            if not vals:
                continue
            blocks = []
            for v in vals:
                if isinstance(v, URIRef):
                    blocks.append(f'<li><a href="{esc(v)}">{esc(v)}</a></li>')
                else:
                    text = esc(v).replace("\n", "<br>")
                    lang = getattr(v, "language", None)
                    tag = f'<span class="lang">@{esc(lang)}</span>' if lang and lang != "en" else ""
                    blocks.append(f"<blockquote>{text}{tag}</blockquote>")
            if all(b.startswith("<li>") for b in blocks):
                out.append(f'<h2>{name}s</h2><ul class="plain">{"".join(blocks)}</ul>')
            else:
                out.append(f'<h2>{name}{"s" if len(blocks) > 1 else ""}</h2>{"".join(blocks)}')
        return "".join(out)

    def generic_table(self, r, skip=HANDLED):
        rows = []
        for p, o in sorted(self.G.predicate_objects(r), key=lambda po: (str(po[0]), str(po[1]))):
            if p in skip:
                continue
            if isinstance(o, BNode):
                inner = "".join(f"<div>{esc(self.curie(p2))}: {self.lit(o2)}</div>"
                                for p2, o2 in self.G.predicate_objects(o))
                rows.append(f"<tr><td>{esc(self.curie(p))}</td><td>{inner}</td></tr>")
            else:
                rows.append(f"<tr><td>{esc(self.curie(p))}</td><td>{self.lit(o)}</td></tr>")
        inv = []
        for s, p in sorted(self.G.subject_predicates(r), key=lambda sp: (str(sp[1]), str(sp[0]))):
            if isinstance(s, BNode) or p in (SKOS.broader, SKOS.narrower, SKOS.inScheme, SKOS.member,
                                              SKOS.hasTopConcept, SKOS.topConceptOf, DCTERMS.hasVersion):
                continue
            inv.append(f"<tr><td>{self.ref(s)}</td><td>{esc(self.curie(p))}</td></tr>")
        out = ""
        if rows:
            out += f'<h2>Other statements</h2><table><tr><th>Property</th><th>Value</th></tr>{"".join(rows)}</table>'
        if inv:
            out += f'<h2>Referenced by</h2><table><tr><th>Resource</th><th>Property</th></tr>{"".join(inv)}</table>'
        return out

    def header(self, r):
        G = self.G
        lbl = label_of(G, r, self.base)
        n = first_lit(G, r, SKOS.notation)
        col = first_lit(G, r, URIRef(self.base + "colour"))
        kind_colour = {SKOS.Concept: "var(--c-classes)", SKOS.Collection: "var(--c-collection)",
                       SKOS.ConceptScheme: "var(--c-scheme)"}
        chips = "".join(f'<span class="chip kind" style="--k:{kind_colour.get(t, "var(--c-other)")}">{esc(self.curie(t))}</span>'
                        for t in types_of(G, r))
        if n:
            chips = f'<span class="chip code">{esc(n)}</span>' + chips
        sw = f'<span class="sw" style="background:{esc(col)}"></span>' if col else ""
        bar = esc(col) if col else next((kind_colour[t] for t in types_of(G, r) if t in kind_colour), "var(--line)")
        h = (f'<div class="hero" style="--hero:{bar}"><h1>{sw}{esc(lbl)}</h1><div>{chips}</div>'
             f'<p class="uri">{esc(r)}</p></div>')
        if (r, OWL.deprecated, Literal(True)) in G:
            rep = list(G.objects(r, DCTERMS.isReplacedBy))
            msg = "This concept is <strong>deprecated</strong>: it is not part of the current NZLUM version."
            if rep:
                msg += " Replaced by " + ", ".join(self.ref(x) for x in rep) + "."
            h += f'<div class="banner">{msg}</div>'
        # alternate labels / other languages
        extra = [v for v in lits(G, r, SKOS.prefLabel) if getattr(v, "language", None) != "en"]
        alt = lits(G, r, SKOS.altLabel)
        if extra or alt:
            h += "<p>" + " · ".join(self.lit(v) for v in extra + alt) + "</p>"
        return h

    def sort_concepts(self, cs):
        G = self.G
        return sorted(cs, key=lambda c: (notation_key(first_lit(G, c, SKOS.notation)), str(label_of(G, c, self.base)), str(c)))

    def nested_list(self, cs, within, cls="plain cols"):
        """List concepts, nesting children (skos:narrower or inverse skos:broader) under their parent
        when both are in `within`."""
        G = self.G
        roots = [c for c in cs if not any(b in within for b in G.objects(c, SKOS.broader))]
        def render(items, cls_):
            out = f'<ul class="{cls_}">'
            for c in self.sort_concepts(items):
                kids = {k for k in G.objects(c, SKOS.narrower) if k in within}
                kids |= {k for k in G.subjects(SKOS.broader, c) if k in within}
                out += f"<li>{self.ref(c)}" + (render(kids, "plain") if kids else "") + "</li>"
            return out + "</ul>"
        return render(roots, cls)

    # ---- concept
    def concept(self, r):
        G, ex = self.G, self.ex
        body = self.header(r)
        body += self.notes(r)

        def sorted_concepts(cs):
            return sorted(cs, key=lambda c: (notation_key(first_lit(G, c, SKOS.notation)), str(c)))

        hier = ""
        broader = list(G.objects(r, SKOS.broader))
        if broader:
            hier += "<dt>Broader</dt><dd>" + "<br>".join(self.ref(b) for b in sorted_concepts(broader)) + "</dd>"
        path = []
        cur, guard = r, 0
        while guard < 10:
            b = next(G.objects(cur, SKOS.broader), None)
            if b is None:
                break
            path.insert(0, b)
            cur, guard = b, guard + 1
        if path:
            hier += "<dt>Path</dt><dd>" + " › ".join(self.ref(b) for b in path) + f" › <strong>{esc(label_of(G, r, self.base))}</strong></dd>"
        tops = list(G.objects(r, SKOS.topConceptOf))
        if tops:
            hier += "<dt>Top concept of</dt><dd>" + "<br>".join(self.ref(s) for s in sorted(tops, key=str)) + "</dd>"
        colls = list(G.subjects(SKOS.member, r))
        if colls:
            hier += "<dt>Member of</dt><dd>" + "<br>".join(self.ref(c) for c in sorted(colls, key=str)) + "</dd>"
        if hier:
            body += f"<h2>Hierarchy</h2><dl>{hier}</dl>"
        narrower = list(G.objects(r, SKOS.narrower))
        if narrower:
            body += "<h2>Narrower</h2><ul class=\"plain\">" + "".join(
                f"<li>{self.ref(c)}</li>" for c in sorted_concepts(narrower)) + "</ul>"

        # versions
        vs = ex.present.get(r, [])
        if vs:
            rows = []
            for v in reversed(vs):
                g = ex.vgraphs[v]
                code = first_lit(g, r, SKOS.notation) or ""
                lbl = first_lit(g, r, SKOS.prefLabel) or ""
                diffs = ex.version_differences(v, r)
                if v == ex.latest:
                    status = "current"
                elif v == vs[-1]:
                    status = "served (last version containing this concept)"
                else:
                    status = "differs: " + ", ".join(diffs) if diffs else "same"

                rows.append(f'<tr><td><a href="{esc(ex.scheme_uri(v))}">NZLUM {esc(v)}</a></td>'
                            f"<td><code>{esc(code)}</code></td><td>{esc(lbl)}</td>"
                            f'<td><a href="{esc(ex.site_page(v, r))}">class page</a> · '
                            f'<a href="{esc(self.base)}code/nzlum{esc(v)}/{esc(code)}">code lookup</a></td>'
                            f"<td>{esc(status)}</td></tr>")
            body += ("<h2>Versions</h2><p>The description above is taken from the most recent version "
                     "containing this concept. Codes can be reassigned between versions, so cite the "
                     "concept URI, or a code together with its version.</p>"
                     "<table><tr><th>Version</th><th>Code</th><th>Label</th><th>Links</th><th>Compared with current</th></tr>"
                     + "".join(rows) + "</table>")
        else:
            schemes = list(G.objects(r, SKOS.inScheme))
            if schemes:
                body += "<h2>In scheme</h2><ul class=\"plain\">" + "".join(
                    f"<li>{self.ref(s)}</li>" for s in sorted(schemes, key=str)) + "</ul>"

        body += self.generic_table(r)
        body += self.formats_section(r)
        return body

    # ---- collection
    def collection(self, r):
        G = self.G
        body = self.header(r) + self.notes(r)
        schemes = list(G.objects(r, SKOS.inScheme))
        if schemes:
            body += "<p>In scheme: " + ", ".join(self.ref(s) for s in schemes) + "</p>"
        members = list(G.objects(r, SKOS.member))
        if members:
            body += f"<h2>Members ({len(members)})</h2>" + self.nested_list(members, set(members))
        body += self.generic_table(r) + self.formats_section(r)
        return body

    # ---- concept scheme
    def scheme(self, r):
        G, ex = self.G, self.ex
        body = self.header(r) + self.notes(r)
        meta = ""
        for p, name in [(OWL.versionInfo, "Version"), (DCTERMS.issued, "Issued"), (ADMS.status, "Status"),
                        (DCTERMS.isVersionOf, "Version of"), (DCTERMS.replaces, "Replaces"),
                        (DCTERMS.isReplacedBy, "Replaced by"), (FOAF.homepage, "Homepage")]:
            vals = list(G.objects(r, p))
            if vals:
                meta += f"<dt>{name}</dt><dd>" + "<br>".join(self.lit(v) for v in vals) + "</dd>"
        versions = list(G.objects(r, DCTERMS.hasVersion))
        if versions:
            meta += "<dt>Versions</dt><dd>" + "<br>".join(
                f"{self.ref(v)} ({esc(first_lit(G, v, OWL.versionInfo) or '')}, "
                f"{esc(label_of(G, next(G.objects(v, ADMS.status), URIRef('')), self.base) if next(G.objects(v, ADMS.status), None) else '')})"
                for v in sorted(versions, key=lambda v: parse_version(first_lit(G, v, OWL.versionInfo) or "0"))) + "</dd>"
        if meta:
            body += f"<h2>About</h2><dl>{meta}</dl>"

        # the concepts of this scheme, as they are *in this version*
        vv = [v for v in ex.versions if ex.scheme_uri(v) == r]
        if r in ex.tgraphs:
            g = ex.tgraphs[r]
        else:
            g = ex.vgraphs[vv[0]] if vv else None
        if g is not None:
            colls = sorted(g.subjects(RDF.type, SKOS.Collection), key=lambda c: str(label_of(g, c, self.base)))
            if colls:
                body += "<h2>Collections</h2><ul class=\"plain\">" + "".join(
                    f"<li>{self.ref(c)} ({len(list(g.objects(c, SKOS.member)))})</li>" for c in colls) + "</ul>"
            tops = list(g.objects(r, SKOS.hasTopConcept))
            concepts = [c for c in g.subjects(SKOS.inScheme, r) if is_a(g, c, SKOS.Concept)]
            if tops:
                body += "<h2>Hierarchy</h2>"
                def tree(cs, depth):
                    cs = sorted(cs, key=lambda c: (notation_key(first_lit(g, c, SKOS.notation)), str(c)))
                    out = "<ul class=\"plain\">"
                    for c in cs:
                        n = first_lit(g, c, SKOS.notation) or ""
                        lbl = first_lit(g, c, SKOS.prefLabel) or label_of(g, c, self.base)
                        out += (f'<li style="padding-left:{depth*1.2}rem"><code>{esc(n)}</code> '
                                f'<a href="{esc(c)}">{esc(lbl)}</a></li>')
                        kids = list(g.objects(c, SKOS.narrower))
                        if kids:
                            out += "<li>" + tree(kids, depth + 1) + "</li>"
                    return out + "</ul>"
                body += tree(tops, 0)
            elif concepts:
                body += f"<h2>Concepts ({len(concepts)})</h2>" + self.nested_list(concepts, set(concepts))
            if vv:
                body += f'<p>Codes in this version: <a href="{self.base}code/nzlum{esc(vv[0])}/">code table</a>.</p>'
            body += ("<h2>Download</h2><p>The RDF documents for this scheme contain the <em>complete</em> "
                     "vocabulary as published in this version, not just the scheme's own metadata.</p>")
        body += self.generic_table(r, skip=HANDLED | {OWL.versionInfo, DCTERMS.issued, ADMS.status, DCTERMS.isVersionOf,
                                                       DCTERMS.replaces, DCTERMS.isReplacedBy, FOAF.homepage, DCTERMS.hasVersion})
        body += self.formats_section(r)
        return body

    def other(self, r):
        return self.header(r) + self.notes(r) + self.generic_table(r) + self.formats_section(r)

    def resource_page(self, r, jsonld):
        G = self.G
        if is_a(G, r, SKOS.Concept):
            body = self.concept(r)
        elif is_a(G, r, SKOS.Collection):
            body = self.collection(r)
        elif is_a(G, r, SKOS.ConceptScheme):
            body = self.scheme(r)
        else:
            body = self.other(r)
        return self.page(label_of(G, r, self.base), body, uri=r, jsonld=jsonld,
                         alternates=self.alternates_for(r), canonical=str(r))

    # ---- code lookups
    def code_pages(self):
        ex, G = self.ex, self.G
        written = 0
        vrows = []
        for v in reversed(ex.versions):
            g = ex.vgraphs[v]
            scheme = ex.scheme_uri(v)
            by_code = defaultdict(list)
            for c in g.subjects(SKOS.inScheme, scheme):
                n = first_lit(g, c, SKOS.notation)
                if n:
                    by_code[n].append(c)
            rows = []
            for code in sorted(by_code, key=notation_key):
                cs = by_code[code]
                if len(cs) > 1:
                    print(f"warning: code {code} is used by {len(cs)} concepts in NZLUM {v}", file=sys.stderr)
                c = sorted(cs, key=str)[0]
                lbl = first_lit(g, c, SKOS.prefLabel) or ""
                cur = first_lit(G, c, SKOS.notation)
                note = "" if cur == code else f"now <code>{esc(cur)}</code>" if cur and not (c, OWL.deprecated, Literal(True)) in G else "deprecated"
                rows.append(f'<tr><td><a href="{esc(self.base)}code/nzlum{esc(v)}/{esc(code)}"><code>{esc(code)}</code></a></td>'
                            f'<td>{esc(lbl)}</td><td><a href="{esc(c)}">{esc(rel_path(c, self.base))}</a></td><td>{note}</td></tr>')
                body = (f"<h1>Code {esc(code)} in NZLUM {esc(v)}</h1>"
                        f"<p>In <a href=\"{esc(scheme)}\">NZLUM {esc(v)}</a>, code <code>{esc(code)}</code> is "
                        f"<strong><a href=\"{esc(c)}\">{esc(lbl)}</a></strong>.</p>"
                        f"<p class=\"uri\">Concept URI: <a href=\"{esc(c)}\">{esc(c)}</a></p>"
                        "<p>This address is a lookup, not an identifier. Codes can be reassigned between versions; "
                        "cite the concept URI, or a code together with its version. "
                        "You are being redirected to the concept.</p>")
                writefile(os.path.join(ex.out, "landuse", "code", f"nzlum{v}", f"{code}.html"),
                          self.page(f"{code} (NZLUM {v})", body, canonical=str(c),
                                    alternates=self.alternates_for(c), refresh=str(c)))
                written += 1
            body = (f"<h1>NZLUM {esc(v)} codes</h1><p>Scheme: <a href=\"{esc(scheme)}\">{esc(scheme)}</a>. "
                    f"Each code links to a page that redirects to the concept URI, so "
                    f"<code>{esc(self.base)}code/nzlum{esc(v)}/&lt;code&gt;</code> can be used as a stable lookup "
                    "for a code <em>within this version</em>.</p>"
                    "<table><tr><th>Code</th><th>Label</th><th>Concept</th><th>In current version</th></tr>"
                    + "".join(rows) + "</table>")
            writefile(os.path.join(ex.out, "landuse", "code", f"nzlum{v}", "index.html"),
                      self.page(f"NZLUM {v} codes", body))
            status = first_lit(G, scheme, OWL.versionInfo)
            st = next(G.objects(scheme, ADMS.status), None)
            vrows.append(f'<li><a href="{esc(self.base)}code/nzlum{esc(v)}/">NZLUM {esc(v)}</a> '
                         f'({esc(label_of(G, st, self.base)) if st else ""}; {len(rows)} codes)</li>')
        body = ("<h1>Code lookup</h1><p>Look up what a numeric NZLUM code meant in a given version. "
                "Pick a version, or go directly to "
                f"<code>{esc(self.base)}code/nzlum&lt;version&gt;/&lt;code&gt;</code>.</p>"
                "<p>Codes are not stable across versions: some have been reassigned to different concepts. "
                "Data records should therefore carry the NZLUM version alongside the code.</p>"
                "<ul class=\"plain\">" + "".join(vrows) + "</ul>")
        writefile(os.path.join(ex.out, "landuse", "code", "index.html"), self.page("Code lookup", body))
        return written

    # ---- namespace index
    def index_page(self, resources):
        ex, G = self.ex, self.G
        body = ('<div class="hero" style="--hero:var(--c-scheme)"><h1>NZLUM vocabulary</h1>'
                f'<p class="uri">{esc(self.base)}</p></div>'
                "<p>Every URI in this namespace resolves to an HTML page like this one, with Turtle, JSON-LD and "
                "RDF/XML available by appending <code>.ttl</code>, <code>.jsonld</code> or <code>.rdf</code>. "
                "SKOS concept schemes are versioned; concept URIs are not.</p>")
        schemes = sorted(G.subjects(RDF.type, SKOS.ConceptScheme), key=str)
        body += '<section class="card card-schemes"><h2>Concept schemes</h2><table><tr><th>Scheme</th><th>Version</th><th>Status</th><th>Concepts</th></tr>'
        for s in schemes:
            st = next(G.objects(s, ADMS.status), None)
            n = len([c for c in G.subjects(SKOS.inScheme, s) if is_a(G, c, SKOS.Concept)])
            vers = list(G.objects(s, DCTERMS.hasVersion))
            count = f"{len(vers)} versions" if vers else str(n)
            body += (f"<tr><td>{self.ref(s)}</td><td>{esc(first_lit(G, s, OWL.versionInfo) or '')}</td>"
                     f"<td>{esc(label_of(G, st, self.base)) if st else ''}</td><td>{count}</td></tr>")
        body += "</table>"
        body += (f'<p><a href="{self.base}code/">Code lookup by version</a> · '
                 f'Everything as <a href="{self.base}all.ttl">Turtle</a>, <a href="{self.base}all.jsonld">JSON-LD</a>, '
                 f'<a href="{self.base}all.rdf">RDF/XML</a></p></section>')
        def li(c, extra=""):
            return f"<li>{self.ref(c)}{extra}</li>"

        sort_concepts = self.sort_concepts

        nested_list = self.nested_list

        # 1. NZLUM classes, current version, as a tree: primaries open, secondaries collapsed
        latest_scheme = ex.scheme_uri(ex.latest)
        n_classes = len([c for c in G.subjects(SKOS.inScheme, latest_scheme) if is_a(G, c, SKOS.Concept)])
        body += (f'<section class="card card-classes"><h2><a href="{esc(latest_scheme)}">NZLUM classes v{esc(ex.latest)}</a> '
                 f'<span class="n">{n_classes} classes · primary › secondary › tertiary</span></h2>')
        for top in sort_concepts(G.objects(latest_scheme, SKOS.hasTopConcept)):
            body += f'<details open><summary>{self.ref(top)}</summary>'
            for sec in sort_concepts(G.objects(top, SKOS.narrower)):
                terts = sort_concepts(G.objects(sec, SKOS.narrower))
                if terts:
                    body += (f'<details><summary>{self.ref(sec)} <span class="n">({len(terts)})</span></summary>'
                             '<ul class="plain cols">' + "".join(li(t) for t in terts) + "</ul></details>")
                else:
                    body += f'<details><summary>{self.ref(sec)}</summary><p class="n">No tertiary classes.</p></details>'
            body += "</details>"
        deprecated = [r for r in resources if (r, OWL.deprecated, Literal(True)) in G]
        if deprecated:
            body += (f'<details><summary>Deprecated concepts <span class="n">({len(deprecated)}, from earlier versions)</span></summary>'
                     '<ul class="plain cols">' + "".join(li(c) for c in sort_concepts(deprecated)) + "</ul></details>")
        body += "</section>"

        # 2. term lists: grouped by skos:Collection where the list has them, flat otherwise
        for scheme in sorted(ex.tgraphs, key=lambda s_: str(label_of(G, s_, self.base))):
            concepts = {c for c in G.subjects(SKOS.inScheme, scheme) if is_a(G, c, SKOS.Concept)}
            colls = sorted((c for c in G.subjects(SKOS.inScheme, scheme) if is_a(G, c, SKOS.Collection)),
                           key=lambda c: str(label_of(G, c, self.base)))
            local = rel_path(scheme, self.base).split("/")[-1]
            card = {"commodities": "card-commodity", "management_practices": "card-mgmt", "water_features": "card-water"}.get(local, "card-other")
            how = f"{len(concepts)} terms in {len(colls)} collections" if colls else f"{len(concepts)} terms"
            body += f'<section class="card {card}"><h2>{self.ref(scheme)} <span class="n">{how}</span></h2>'
            if colls:
                placed = set()
                for coll in colls:
                    members = [m for m in G.objects(coll, SKOS.member) if m in concepts]
                    placed.update(members)
                    body += (f'<details><summary>{self.ref(coll)} <span class="n">({len(members)})</span></summary>'
                             + nested_list(members, set(members)) + "</details>")
                rest = concepts - placed
                if rest:
                    body += (f'<details><summary>Not in any collection <span class="n">({len(rest)})</span></summary>'
                             + nested_list(rest, rest) + "</details>")
            else:
                body += nested_list(concepts, concepts)
            body += "</section>"

        # 3. everything else in the namespace
        other = [r for r in resources if not is_a(G, r, SKOS.Concept) and not is_a(G, r, SKOS.Collection)
                 and not is_a(G, r, SKOS.ConceptScheme)]
        if other:
            body += (f'<section class="card card-other"><h2>Other resources <span class="n">{len(other)}</span></h2><ul class="plain cols">'
                     + "".join(f"<li>{self.ref(r)} <span class=\"n\">{esc(', '.join(self.curie(t) for t in types_of(G, r)))}</span></li>"
                               for r in sorted(other, key=str)) + "</ul></section>")
        return self.page("NZLUM vocabulary", body, canonical=self.base,
                         alternates=[(f"{self.base}all.{ext}", mime, name) for ext, mime, _, name in FORMATS])


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", help="output directory (the tree starts at <out>/landuse/)")
    ap.add_argument("--base", default="https://nzlum.landcareresearch.co.nz/landuse/")
    ap.add_argument("--site", default="https://nzlum.landcareresearch.co.nz")
    ap.add_argument("--version", action="append", required=True, metavar="VER=TTL",
                    help="an NZLUM version and the built Turtle file for it (repeatable)")
    ap.add_argument("--term-list", action="append", default=[], metavar="TTL",
                    help="an unversioned term-list Turtle file (repeatable)")
    a = ap.parse_args()

    versions = {}
    for spec in a.version:
        v, _, path = spec.partition("=")
        if not path:
            ap.error(f"--version expects VER=PATH, got {spec}")
        versions[v] = path

    ex = Exporter(a.out, a.base, a.site, versions, a.term_list)
    hw = HtmlWriter(ex)
    resources = ex.resources()
    print(f"served graph: {len(ex.G)} triples; {len(resources)} resources; versions {ex.versions}")

    for r in resources:
        d = ex.describe(r)
        noext = os.path.join(a.out, "landuse", rel_path(r, ex.base))
        ex.write_rdf(noext, d)
        jsonld = prune_jsonld_context(d.serialize(format="json-ld", auto_compact=True))
        writefile(noext + ".html", hw.resource_page(r, jsonld))

    writefile(os.path.join(a.out, "landuse", "nzlum-ld.css"), CSS.strip() + "\n")
    ex.write_rdf(os.path.join(a.out, "landuse", "all"), ex.G)
    writefile(os.path.join(a.out, "landuse", "index.html"), hw.index_page(resources))
    n_codes = hw.code_pages()
    print(f"wrote {len(resources)} resources x {len(FORMATS) + 1} documents, {n_codes} code lookups, under {a.out}/landuse/")


if __name__ == "__main__":
    main()
