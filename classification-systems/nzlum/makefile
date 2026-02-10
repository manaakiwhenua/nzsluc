DATA = rdf/scheme.ttl rdf/concepts-1.ttl rdf/concepts-2.ttl rdf/concepts-3.ttl
BUILD = build

$(BUILD)/nzlum.ttl: $(DATA)
	mkdir -p $(BUILD)
	riot --validate $(DATA)
	riot --output=turtle $(DATA) > $(BUILD)/nzlum.ttl

.PHONY: tables-all
tables-all: $(BUILD)/nzlum.ttl
	@for scheme in $$(./scripts/list_versions.py rdf/scheme.ttl); do \
	  ver=$$(echo $$scheme | sed -E 's#.*/nzlum##'); \
	  echo "Generating tables for $$scheme (version $$ver)"; \
	  ./scripts/export_table.py $(BUILD)/nzlum.ttl $$scheme \
	    $(BUILD)/nzlum_v$${ver}.md $(BUILD)/nzlum_v$${ver}.xlsx ; \
	done


.PHONY: shacl
shacl: $(BUILD)/nzlum.ttl
	shacl validate --shapes shapes/shapes.ttl --data $(BUILD)/nzlum.ttl

.PHONY: outline-all
outline-all: $(BUILD)/nzlum.ttl
	@for scheme in $$(./scripts/list_versions.py rdf/scheme.ttl); do \
	  ver=$$(echo $$scheme | sed -E 's#.*/nzlum##'); \
	  echo "Generating outline for $$scheme (version $$ver)"; \
	  ./scripts/export_outline.py $(BUILD)/nzlum.ttl $$scheme \
	    $(BUILD)/nzlum_v$${ver}_outline.md ; \
	done