## Tool installation

Linux instructions for installing Apache Jena for the purposes of validating Turtle.

```bash
# Install Java 21 (required for Jena 6)
sudo dnf install java-21-openjdk
java -version

# Download and install Apache Jena 6.0.0 binaries
cd /tmp
curl -LO https://dlcdn.apache.org/jena/binaries/apache-jena-6.0.0.tar.gz
# Verify the download
curl -LO https://dlcdn.apache.org/jena/binaries/apache-jena-6.0.0.tar.gz.sha512
sha512sum -c apache-jena-6.0.0.tar.gz.sha512
tar -xzf apache-jena-6.0.0.tar.gz
sudo mv apache-jena-6.0.0 /opt/

# Add Jena commands to your PATH
sudo tee /etc/profile.d/jena.sh > /dev/null <<'EOF'
export JENA_HOME=/opt/apache-jena-6.0.0
export PATH="$JENA_HOME/bin:$PATH"
EOF

# Reload environment
source /etc/profile.d/jena.sh

# Verify it works
riot --version
sparql --version
```

## Validation

Now you can validate:

```bash
riot --validate nzlum.ttl
```

Run SPARQL directly over the TTL (no TDB):

```bash
sparql --data nzlum.ttl --query validation/count.rq # Other sanity-checking queries avaialble as *.rq
```

### Constraints

SHACL is used as a validation rule-set to check the SKOS vocabulary is complete and consistent.

- `nzlum.ttl` is the SKOS vocabulary file (the data)
- `shapes.ttl` is the SHACL shapes file (the constraints)

```bash
shacl validate --shapes shapes.ttl --data nzlum.ttl
```

This is in preference to the example queries in .validation/

## Visualisation

```bash
pip install openpyxl
```

```bash
SCHEME=nzlum0.4.0 && python scripts/export-table.py nzlum.ttl https://example.org/landuse/scheme/$SCHEME $SCHEME.md $SCHEME.xlsx
```


### TODO
- [x] Install Apache Jena
- [x] Validate with Jena's riot command: `riot --validate nzlum.ttl`
- [x] Load it and run simple sanity queries with Jena's tdbloader and sparql command line tools
- [x] Use SHACL to validate the structure of the concept scheme
- [x] Scipt for generating an SVG diagram showing hierarchy and relationships between concepts, notation and labels
- [ ] Add more concepts and relationships


