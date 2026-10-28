#!/usr/bin/env python3
"""Serve a static directory the way GitHub Pages does, for local testing.

    ./scripts/serve_static.py build/www            # then open http://localhost:8000/landuse/
    ./scripts/serve_static.py ~/Documents/nzlum-site/dist

Like GitHub Pages it serves "foo.html" for a request to "/foo" (no redirect),
"dir/index.html" for "/dir/", and the RDF serialisations with their proper
media types. No dependencies beyond the standard library.
"""
import http.server
import os
import sys

MIME = {
    ".ttl": "text/turtle; charset=utf-8",
    ".jsonld": "application/ld+json",
    ".rdf": "application/rdf+xml",
    ".qml": "application/xml",
    ".sld": "application/xml",
    ".mss": "text/plain; charset=utf-8",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, **MIME}

    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and not p.endswith("/") and os.path.isfile(p + ".html"):
            return p + ".html"
        return p

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, fmt % args))


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    os.chdir(root)
    print(f"serving {os.getcwd()} at http://localhost:{port}/  (Ctrl-C to stop)")
    http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
