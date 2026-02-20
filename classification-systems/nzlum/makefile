VERSION = 0.4.0
SCHEME = https://nzlum.landcareresearch.co.nz/landuse/scheme/nzlum$(VERSION)
DATA = rdf/scheme.ttl rdf/$(VERSION)/concepts*.ttl
BUILD = build

$(BUILD)/nzlum-$(VERSION).ttl: $(DATA)
	mkdir -p $(BUILD)
	riot --validate $(DATA)
	riot --output=turtle $(DATA) > $(BUILD)/nzlum-$(VERSION).ttl

.PHONY: tables-all
tables-all: $(BUILD)/nzlum-$(VERSION).ttl
	./scripts/export_table.py $(BUILD)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(BUILD)/nzlum_v$(VERSION).md $(BUILD)/nzlum_v$(VERSION).xlsx ;

.PHONY: shacl
shacl: $(BUILD)/nzlum-$(VERSION).ttl
	shacl validate --shapes shapes/shapes.ttl --data $(BUILD)/nzlum-$(VERSION).ttl

.PHONY: outline-all
outline-all: $(BUILD)/nzlum-$(VERSION).ttl
	./scripts/export_outline.py $(BUILD)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(BUILD)/nzlum_v$(VERSION)_outline.md ;

.PHONY: collections-all
collections-all:
	mkdir -p $(BUILD)
	@echo "Generating commodities collection export..."; \
	./scripts/export_collections.py rdf/term-lists/commodities.ttl lus:commodities \
	  $(BUILD)/commodities.md $(BUILD)/commodities.xlsx ; \
	echo "Generating management practices collection export..."; \
	./scripts/export_collections.py rdf/term-lists/management-practices.ttl lus:management_practices \
	  $(BUILD)/management_practices.md $(BUILD)/management_practices.xlsx

clean:
	rm -rf $(BUILD)