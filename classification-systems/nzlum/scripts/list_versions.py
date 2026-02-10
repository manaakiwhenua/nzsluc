#!/usr/bin/env python3
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
import sys

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT  = Namespace("http://purl.org/dc/terms/")

g = Graph()
g.parse(sys.argv[1], format="turtle")

# find the series scheme (no dct:isVersionOf), then list dct:hasVersion
series = [s for s in g.subjects(RDF.type, SKOS.ConceptScheme)
          if (s, DCT.isVersionOf, None) not in g]

# If multiple, just emit all versions from all series schemes
versions = set()
for s in series:
    for v in g.objects(s, DCT.hasVersion):
        versions.add(str(v))

for v in sorted(versions):
    print(v)