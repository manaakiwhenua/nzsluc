#!/usr/bin/env python3
"""Generate a one-page SVG summary table of the classification hierarchy.

One column per primary (top) concept; within each column, one bordered box
per secondary concept, whose first row is the secondary concept and whose
remaining rows are its tertiary concepts. Cells are filled with the
concept's lu:colour where one exists, and otherwise with a grey shaded by
depth (dark/medium/light for primary/secondary/tertiary). Label text is
black or white, whichever contrasts better with the fill.

No other information from the classification system is included.

Usage: export_svg_summary.py INPUT.ttl SCHEME_IRI OUTPUT.svg TITLE
"""
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
LU = Namespace("https://nzlum.landcareresearch.co.nz/landuse/")

# Fallback fills, by depth, when a concept carries no lu:colour
GREY_PRIMARY = "#8C8C8C"
GREY_SECONDARY = "#B8B8B8"
GREY_TERTIARY = "#E0E0E0"

FONT = "Helvetica, Arial, 'DejaVu Sans', sans-serif"
FONT_SIZE = 9.5
TITLE_SIZE = 14
LINE_HEIGHT = 11.5
CELL_PAD_X = 6
CELL_PAD_Y = 3
# Drop from the top of a line box to its baseline
BASELINE_DROP = 8.6
COL_WIDTH = 260
COL_GAP = 10
BOX_GAP = 8
MARGIN = 12
TITLE_GAP = 14
# Gap between a concept's code and the label column it hangs beside
CODE_GAP = 8
STROKE = "#000000"

# Glyph advances as a fraction of the font size, from Liberation Sans, which
# is metric-compatible with the Arial/Helvetica faces named in FONT. Baked in
# so wrapping does not depend on a font file being installed at build time.
ADVANCE_REGULAR = {
    ' ': 0.2778, '!': 0.2778, '"': 0.355, '#': 0.5562, '$': 0.5562, '%': 0.8892, '&': 0.667,
    "'": 0.1909, '(': 0.333, ')': 0.333, '*': 0.3892, '+': 0.584, ',': 0.2778, '-': 0.333,
    '.': 0.2778, '/': 0.2778, '0': 0.5562, '1': 0.5562, '2': 0.5562, '3': 0.5562, '4': 0.5562,
    '5': 0.5562, '6': 0.5562, '7': 0.5562, '8': 0.5562, '9': 0.5562, ':': 0.2778, ';': 0.2778,
    '<': 0.584, '=': 0.584, '>': 0.584, '?': 0.5562, '@': 1.0151, 'A': 0.667, 'B': 0.667,
    'C': 0.7222, 'D': 0.7222, 'E': 0.667, 'F': 0.6108, 'G': 0.7778, 'H': 0.7222, 'I': 0.2778,
    'J': 0.5, 'K': 0.667, 'L': 0.5562, 'M': 0.833, 'N': 0.7222, 'O': 0.7778, 'P': 0.667,
    'Q': 0.7778, 'R': 0.7222, 'S': 0.667, 'T': 0.6108, 'U': 0.7222, 'V': 0.667, 'W': 0.9438,
    'X': 0.667, 'Y': 0.667, 'Z': 0.6108, '[': 0.2778, '\\': 0.2778, ']': 0.2778, '^': 0.4692,
    '_': 0.5562, '`': 0.333, 'a': 0.5562, 'b': 0.5562, 'c': 0.5, 'd': 0.5562, 'e': 0.5562,
    'f': 0.2778, 'g': 0.5562, 'h': 0.5562, 'i': 0.2222, 'j': 0.2222, 'k': 0.5, 'l': 0.2222,
    'm': 0.833, 'n': 0.5562, 'o': 0.5562, 'p': 0.5562, 'q': 0.5562, 'r': 0.333, 's': 0.5,
    't': 0.2778, 'u': 0.5562, 'v': 0.5, 'w': 0.7222, 'x': 0.5, 'y': 0.5, 'z': 0.5, '{': 0.334,
    '|': 0.2598, '}': 0.334, '~': 0.584, '\u00e8': 0.5562, '\u00e9': 0.5562, '\u0101': 0.5562,
    '\u012b': 0.2778, '\u014d': 0.5562, '\u016b': 0.5562, '\u2013': 0.5562, '\u2014': 1.0,
    '\u2018': 0.2222, '\u2019': 0.2222, '\u201c': 0.333, '\u201d': 0.333,
}
ADVANCE_BOLD = {
    ' ': 0.2778, '!': 0.333, '"': 0.4741, '#': 0.5562, '$': 0.5562, '%': 0.8892, '&': 0.7222,
    "'": 0.2378, '(': 0.333, ')': 0.333, '*': 0.3892, '+': 0.584, ',': 0.2778, '-': 0.333,
    '.': 0.2778, '/': 0.2778, '0': 0.5562, '1': 0.5562, '2': 0.5562, '3': 0.5562, '4': 0.5562,
    '5': 0.5562, '6': 0.5562, '7': 0.5562, '8': 0.5562, '9': 0.5562, ':': 0.333, ';': 0.333,
    '<': 0.584, '=': 0.584, '>': 0.584, '?': 0.6108, '@': 0.9751, 'A': 0.7222, 'B': 0.7222,
    'C': 0.7222, 'D': 0.7222, 'E': 0.667, 'F': 0.6108, 'G': 0.7778, 'H': 0.7222, 'I': 0.2778,
    'J': 0.5562, 'K': 0.7222, 'L': 0.6108, 'M': 0.833, 'N': 0.7222, 'O': 0.7778, 'P': 0.667,
    'Q': 0.7778, 'R': 0.7222, 'S': 0.667, 'T': 0.6108, 'U': 0.7222, 'V': 0.667, 'W': 0.9438,
    'X': 0.667, 'Y': 0.667, 'Z': 0.6108, '[': 0.333, '\\': 0.2778, ']': 0.333, '^': 0.584,
    '_': 0.5562, '`': 0.333, 'a': 0.5562, 'b': 0.6108, 'c': 0.5562, 'd': 0.6108, 'e': 0.5562,
    'f': 0.333, 'g': 0.6108, 'h': 0.6108, 'i': 0.2778, 'j': 0.2778, 'k': 0.5562, 'l': 0.2778,
    'm': 0.8892, 'n': 0.6108, 'o': 0.6108, 'p': 0.6108, 'q': 0.6108, 'r': 0.3892, 's': 0.5562,
    't': 0.333, 'u': 0.6108, 'v': 0.5562, 'w': 0.7778, 'x': 0.5562, 'y': 0.5562, 'z': 0.5,
    '{': 0.3892, '|': 0.2798, '}': 0.3892, '~': 0.584, '\u00e8': 0.5562, '\u00e9': 0.5562,
    '\u0101': 0.5562, '\u012b': 0.2778, '\u014d': 0.6108, '\u016b': 0.6108, '\u2013': 0.5562,
    '\u2014': 1.0, '\u2018': 0.2778, '\u2019': 0.2778, '\u201c': 0.5, '\u201d': 0.5,
}
# Advance assumed for any glyph missing from the tables above
DEFAULT_ADVANCE = 0.6


def get_lang_pref(g, s, p, lang="en"):
    vals = list(g.objects(s, p))
    for v in vals:
        if getattr(v, "language", None) == lang:
            return str(v)
    return str(vals[0]) if vals else None


def notation(g, c):
    n = next(g.objects(c, SKOS.notation), None)
    return str(n) if n else ""


def colour(g, c):
    n = next(g.objects(c, LU.colour), None)
    return str(n) if n else None


def code_key(code):
    try:
        return [int(x) for x in code.split(".")]
    except Exception:
        return [code]


def text_colour(fill_hex):
    """Black or white, whichever contrasts better with `fill_hex` (WCAG)."""
    h = fill_hex.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    # Contrast ratio against white vs. black; 0.179 is the crossover point
    return "#000000" if luminance > 0.179 else "#FFFFFF"


def text_width(text, size=FONT_SIZE, bold=False):
    """Rendered width of `text`, in user units."""
    table = ADVANCE_BOLD if bold else ADVANCE_REGULAR
    return sum(table.get(ch, DEFAULT_ADVANCE) for ch in text) * size


def wrap(text, max_width, bold=False):
    """Greedy word wrap on measured width; over-long single words overflow."""
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        if text_width(f"{cur} {w}", bold=bold) <= max_width:
            cur = f"{cur} {w}"
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


class Cell:
    def __init__(self, code, label, fill, depth):
        self.fill = fill
        self.depth = depth
        self.code = code
        self.label = label
        self.bold = depth < 2

    def layout(self, indent):
        """Wrap the label into the column that starts `indent` in from the text
        origin, so continuation lines hang beside the code rather than under
        it."""
        self.indent = indent
        avail = COL_WIDTH - 2 * CELL_PAD_X - indent
        self.lines = wrap(self.label, avail, bold=self.bold)
        self.height = len(self.lines) * LINE_HEIGHT + 2 * CELL_PAD_Y


def build_tree(g, scheme_iri):
    scheme = URIRef(scheme_iri)
    concepts = {c for c in g.subjects(RDF.type, SKOS.Concept) if (c, SKOS.inScheme, scheme) in g}
    if not concepts:
        raise SystemExit(f"No skos:Concept with skos:inScheme {scheme_iri} found")

    tops = [c for c in g.objects(scheme, SKOS.hasTopConcept) if c in concepts]
    if not tops:
        raise SystemExit(f"No skos:hasTopConcept found for scheme {scheme_iri}")

    children = defaultdict(list)
    for child in concepts:
        for parent in g.objects(child, SKOS.broader):
            if parent in concepts:
                children[parent].append(child)

    def sort_nodes(nodes):
        return sorted(nodes, key=lambda c: (code_key(notation(g, c)),
                                            (get_lang_pref(g, c, SKOS.prefLabel) or "").lower()))

    return sort_nodes(tops), children, sort_nodes


def make_cell(g, concept, depth):
    fallback = (GREY_PRIMARY, GREY_SECONDARY, GREY_TERTIARY)[min(depth, 2)]
    return Cell(
        notation(g, concept),
        get_lang_pref(g, concept, SKOS.prefLabel) or str(concept),
        colour(g, concept) or fallback,
        depth,
    )


def build_columns(g, scheme_iri):
    """[(header Cell, [box]) ...] where a box is a list of Cells."""
    tops, children, sort_nodes = build_tree(g, scheme_iri)
    columns = []
    for top in tops:
        boxes = []
        for secondary in sort_nodes(children.get(top, [])):
            box = [make_cell(g, secondary, 1)]
            box += [make_cell(g, t, 2) for t in sort_nodes(children.get(secondary, []))]
            boxes.append(box)
        columns.append((make_cell(g, top, 0), boxes))

    # One shared label column across the whole figure, set by the widest code
    cells = [c for header, boxes in columns for c in [header] + [c for b in boxes for c in b]]
    indent = max(text_width(c.code, bold=c.bold) for c in cells) + CODE_GAP
    for c in cells:
        c.layout(indent)
    return columns


def render(columns, title):
    def column_height(header, boxes):
        h = header.height + BOX_GAP
        for box in boxes:
            h += sum(c.height for c in box) + BOX_GAP
        return h - BOX_GAP

    body_height = max(column_height(h, b) for h, b in columns)
    width = 2 * MARGIN + len(columns) * COL_WIDTH + (len(columns) - 1) * COL_GAP
    title_block = TITLE_SIZE + TITLE_GAP
    height = 2 * MARGIN + title_block + body_height

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="{FONT}">',
        f'  <rect width="{width:.0f}" height="{height:.0f}" fill="#FFFFFF"/>',
        f'  <text x="{MARGIN}" y="{MARGIN + TITLE_SIZE:.1f}" font-size="{TITLE_SIZE}" '
        f'font-weight="bold" fill="#000000">{escape(title)}</text>',
    ]

    def draw_group(cells, x, y):
        """Draw one bordered box of stacked cells; return its height."""
        total = sum(c.height for c in cells)
        out.append(f'  <g>')
        cy = y
        for cell in cells:
            weight = "bold" if cell.bold else "normal"
            out.append(
                f'    <rect x="{x:.1f}" y="{cy:.1f}" width="{COL_WIDTH}" height="{cell.height:.1f}" '
                f'fill="{cell.fill}" stroke="{STROKE}" stroke-width="0.6"/>'
            )
            fg = text_colour(cell.fill)
            ty = cy + CELL_PAD_Y + BASELINE_DROP
            if cell.code:
                out.append(
                    f'    <text x="{x + CELL_PAD_X:.1f}" y="{ty:.1f}" font-size="{FONT_SIZE}" '
                    f'font-weight="{weight}" fill="{fg}">{escape(cell.code)}</text>'
                )
            lx = x + CELL_PAD_X + cell.indent
            for line in cell.lines:
                out.append(
                    f'    <text x="{lx:.1f}" y="{ty:.1f}" font-size="{FONT_SIZE}" '
                    f'font-weight="{weight}" fill="{fg}">{escape(line)}</text>'
                )
                ty += LINE_HEIGHT
            cy += cell.height
        out.append(
            f'    <rect x="{x:.1f}" y="{y:.1f}" width="{COL_WIDTH}" height="{total:.1f}" '
            f'fill="none" stroke="{STROKE}" stroke-width="1.4"/>'
        )
        out.append('  </g>')
        return total

    x = MARGIN
    top_y = MARGIN + title_block
    for header, boxes in columns:
        y = top_y
        y += draw_group([header], x, y) + BOX_GAP
        for box in boxes:
            y += draw_group(box, x, y) + BOX_GAP
        x += COL_WIDTH + COL_GAP

    out.append('</svg>')
    return "\n".join(out) + "\n"


def main():
    if len(sys.argv) != 5:
        print("Usage: export_svg_summary.py INPUT.ttl SCHEME_IRI OUTPUT.svg TITLE", file=sys.stderr)
        sys.exit(2)

    in_ttl, scheme_iri, out_svg, title = sys.argv[1:5]

    g = Graph()
    g.parse(in_ttl, format="turtle")

    columns = build_columns(g, scheme_iri)
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(render(columns, title))

    n = sum(1 + sum(len(box) for box in boxes) for _, boxes in columns)
    print(f"Wrote {out_svg} ({len(columns)} columns, {n} concepts)", file=sys.stderr)


if __name__ == "__main__":
    main()
