VERSION = 0.4.0
VERSIONS = 0.3.0 0.4.0
SCHEME = https://nzlum.landcareresearch.co.nz/landuse/scheme/nzlum$(VERSION)
DATA = rdf/scheme.ttl rdf/$(VERSION)/concepts*.ttl
BUILD = build
OUT = $(BUILD)/$(VERSION)
WATER = rdf/term-lists/water-features.ttl
WATER_SCHEME = https://nzlum.landcareresearch.co.nz/landuse/scheme/water_features

.PHONY: all
all: mdx-all tables-all html-all pdf-all outline-all svg-summary collections-all qgis-style cartocss-style sld-style

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

.PHONY: svg-summary
svg-summary: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_svg_summary.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(OUT)/nzlum_v$(VERSION)_summary.svg "NZLUM v$(VERSION)" ;

.PHONY: qgis-style
qgis-style: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_qgis_style.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	$(WATER) $(WATER_SCHEME) $(OUT)/nzlum_v$(VERSION).qml ;

.PHONY: cartocss-style
cartocss-style: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_cartocss_style.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	'#nzlum' $(OUT)/nzlum_v$(VERSION).mss ;

.PHONY: sld-style
sld-style: $(OUT)/nzlum-$(VERSION).ttl
	./scripts/export_sld_style.py $(OUT)/nzlum-$(VERSION).ttl $(SCHEME) \
	nzlum $(OUT)/nzlum_v$(VERSION).sld ;

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
