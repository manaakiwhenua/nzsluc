VERSION = 0.4.0
VERSIONS = 0.3.0 0.4.0
SCHEME = https://nzlum.landcareresearch.co.nz/landuse/scheme/nzlum$(VERSION)
DATA = rdf/scheme.ttl rdf/$(VERSION)/concepts*.ttl
BUILD = build
OUT = $(BUILD)/$(VERSION)

.PHONY: all
all: mdx-all tables-all html-all pdf-all outline-all collections-all

.PHONY: all-versions
all-versions:
	@for v in $(VERSIONS); do \
		echo "== VERSION=$$v =="; \
		$(MAKE) VERSION=$$v all; \
	done

$(OUT)/nzlum-$(VERSION).ttl: $(DATA)
	mkdir -p $(OUT)
	riot --validate $(DATA)
	riot --output=turtle $(DATA) > $(OUT)/nzlum-$(VERSION).ttl

.PHONY: mdx-all
mdx-all: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_outline_mdx.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(OUT)/nzlum_v$(VERSION)_mdx/ ;

.PHONY: tables-all
tables-all: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_table.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(OUT)/nzlum_v$(VERSION).md $(OUT)/nzlum_v$(VERSION).xlsx ;

.PHONY: html-all
html-all: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_html.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(OUT)/nzlum_v$(VERSION).html "NZLUM v$(VERSION)" ;

.PHONY: pdf-all
pdf-all: html-all
	weasyprint $(OUT)/nzlum_v$(VERSION).html $(OUT)/nzlum_v$(VERSION).pdf ;

.PHONY: shacl
shacl: $(OUT)/nzlum-$(VERSION).ttl
	shacl validate --shapes shapes/shapes.ttl --data $(OUT)/nzlum-$(VERSION).ttl

.PHONY: validate
validate: $(OUT)/nzlum-$(VERSION).ttl
	@for q in validation/*.rq; do \
		echo "== $$q =="; \
		sparql --data $(OUT)/nzlum-$(VERSION).ttl --query $$q; \
	done

.PHONY: outline-all
outline-all: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_outline.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(OUT)/nzlum_v$(VERSION)_outline.md ;

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
