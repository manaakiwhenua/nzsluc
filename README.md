# NZSLUC

[![CC BY 4.0][cc-by-shield]][cc-by]

**THIS IS AN UNPUBLISHED AND UNREVIEWED DRAFT**

[![manaakiwhenua-standards](https://github.com/manaakiwhenua/nzsluc/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

New Zealand currently lacks a comprehensive and cohesive land use information system. There is a lack of consistent definition or approach to mapping land use. Consistent land use information for New Zealand (over space and time) would improve the understanding of the impacts of land use on ecosystem services, support the modelling of the impacts of climate change, and help profile natural disaster risks, among other benefits.

Many land use classifications have been developed for New Zealand, primarily drawing on the same (or very similar) public and commercial data. Few, if any, having been re-used. One of the common reasons for this outcome is that systems tend to narrowly focus and use data that is tightly coupled to one specific application.

We propose that any New Zealand land use classification system adheres to common principles in a common framework.  This document is an initial draft of such a framework.

We propose a **land use classification _framework_** that includes principles and best practices appropriate for any land use classification system (and associated output, i.e. geospatial information and maps). This must allow for multiple land use classifications systems, each with its own intended use cases, potentially across multiple value systems. This may (or may not) include hierarchies for generalisation as well as other types of relational information such as lineage, parts, and/or terminological variation. Multiple hierarchies are important as they will facilitate 1 to 1, 1 to many, many to 1, and many to many relationships as appropriate; even if all that can be captured is that there _is a_ relation between two classes despite not fully understanding how the classes may be related. <!--  --- e.g `skos:related`. -->

We propose that **land use classification _systems_** are developed within this framework. It is at the _system_ level that a more concrete set of classes may be designed. It is unlikely that one classification _system_ will be appropriate for all data or use cases. This allows for the development of multiple systems using a variety of properties, potentially only available at specific spatial or temporal scales, limited extents, or specific purposes (including confidentiality).

# The New Zealand Standard Land Use Classification Framework

The NZSLUC Framework presents principles and best practices for designing land use classification systems.

Principles are intended to guide practitioners in how they use, re-use or design classification systems.

> **Kua raranga tahi tatou he whāriki, mātauranga mō āpōpō.**
> 
> _Together we weave the mat / In terms of [mātauranga](https://maoridictionary.co.nz/word/3830) / For future generations._

This [whakataukī](https://maoridictionary.co.nz/word/9903) envisions a mat weaving analogy which in this context brings to mind the reliance on multiple independent sources of input data, information, and knowledge from different people and organisations, with the ultimate aim of creating a shared understanding of land use as spatial information. A land use map can be used by and for future generations to answer the enduring questions they will have about land.

## Principles <!-- Informative -->

1. #### Prioritise atomic data (i.e. decomposition of multidimensional attributes, e.g. tenure)
    - Break down information being collected into individual (atomic, primitive, indivisible) attributes.
    - Collect primary data in place of secondary categorical data, where feasible.
1. #### Be specific about purpose and scope
    - Each classification is designed for an explicit spatiotemporal geographic unit.
    - Atomic geographic units, such as DGGS zones, should be preferred over pre-existing geographic units such as proepty boundaries.
    - A classification system does not have to be comprehensive, and may consider some land use types "out of scope", according to the purpose.
1. #### Classification systems should be extensible
    - Ensure flexibility for land use classification systems which support indigenous data sovereignty protocols (see [Te Mana Raraunga – Māori Data Sovereignty Network)](https://www.temanararaunga.maori.nz/)).
1. #### Hierarchies are encouraged where appropriate
    - This will allow for both generalisation hierarchies (aggregation/disaggregation) and genealogical hierarchies (lineage). 
1. #### This classification framework is intended to be improved over time
    - The classification framework shall be reviewed based on comments and requests of stakeholders.
    - In particular, the publication of the ISO 19144-3 standard (_Geographic information – Classification Systems – Part 3 Land Use Meta Language (LUML)_) shall cause a revision of these principles and best practices.
1. #### Prioritise reproducible and transparent methodologies 
    - User confidence increases when methodologies can be verified independently.
1. #### Classification systems shall accomodate multiple (e.g. co-located, secondary) land-uses
    - Differentiate between secondary land use (same place, same time) with intra-period land use variation (same place, different time)-- e.g., rotational grazing, summer housing, etc.


## Best practices <!-- Normative -->

<!-- 1. To balance **reliability, practicality, and cost effectiveness** when determining best practices. -->

This collection of best practices are intended for producers of land use information, to benefit consumers of land use information. <!-- Producers are often consumers! -->

The list of best practices for land use classification systems under this framework is below. Separate files add detail.

<!-- 1. Data product specification, e.g. ISO 19131:2022 -->
1. **Purpose** Land use classification systems shall describe their intended use-cases.
1. **Scope** Land use classification systems shall describe their intended scope.
1. **Extensibility** Ensure flexibility for land use classification systems to interact with Māori attribute layers that maintain indigenous data sovereignty.
1. **Description of data quality** The quality of published land use data shall be described using a standard, e.g. ISO 19157-1:2023.
1. **Semantic versioning** Changes made to land use classification systems (including geographic unit or scale) shall be communicated to users using semantic versioning of the form `major.minor.patch`, e.g. v0.2.4. Once a version has been released, the contents of that version must not be modified; modifications must be released as a new version.
1. **Metadata** land use datasets and classiication schema should be published using established metadata standards.
1. **Compatibility and re-use** Compatibility with existing New Zealand classification systems shall be preferred. Compatibility with international classification systems may also be relevant.
1. **Definition of land** Classification systems shall individually determine the definition of "land" with reference to their stated purpose, e.g. whether it is inclusive of marine features.
1. **Primary land use** A justification should be given for the choice of primary land uses (e.g. land area, economic value, duration).
1. **Provenance** Source information (i.e. geographic scale, time/date, operator, and confidence) shall be recorded.


<!-- ![a worked example](figs/Framework-Classification-01.png)
Fig N. Overview figure. -->

### Purpose

Different land use maps are made for different intended purposes, because of the necessity of making decisions about how information is organised that constrain its appliciblity. It is a best practice to explicitly state the purpose for which land use classification systems are designed. This purpose will inform other decisions. When deciding on this purpose, consider what questions are likely to be answered if land use information is systematically organised according to the classification system. A 2013 Stats NZ report[^2] provides a useful framing for these questions as "enduring", i.e. questions that don't really change over time, but the way we answer them (under a type of system or architecture) does.

A choice of geographic unit that make extension and re-organisation of land use information difficult (such as property parcels) can be made for _pragmatic_ reasons, but should be justified. Possible justifications include: alignment with existing tools or published data, computational feasibility, the expected absense of finer-scale input data, restrictions on the use of required input data, or privacy. Where possible, a specification to use grids without pre-defined boundaries (such as [DGGS zones](https://docs.ogc.org/as/20-040r3/20-040r3.html), or raster grids) should be preferred.

### Scope

Land use classification systems _may_ only consider a few land use types, and consider others as being "out of scope". For example, a classification of protected land may choose to classify all other land as "non-protected" without attempting any form of further classification, according to the purpose of that classification system.

### Extensibility

It should always be possible to "extend" or "widen" a classification system with more properties/attributes that can be determined by other users, such that information can be re-organised, re-presented, and corrected according to local priorities, to be owned by hapū and iwi without an expectation that this will be visible "upstream". 

Allowing both a class hierarchy and the annotation of multiple attributes is intended to enable the representation of whakapapa and whanaungatanga (the origins, interdependencies, and interconnections) within a land use classification system; and to represent the multiplicity of uses any area of land can simultaneously be associated with, that may go beyond the original intended purpose of a land use classification system.

### Data quality

<!-- Justification? -->
<!-- Alternative standards? -->
<!-- Proposed/example validation procedures? -->

### Semantic versioning

- Major version for backwards incompatible functionality.
    - Major version 0 is reserved for initial development and tolerance for change is higher than for other major versions.
- Minor version for new or modified functionality in a backwardly compatible manner.
- Patch version for backwardly compatible fixes and minor adjustments.

### Metadata

One or more established metadata standards shall be used when publishing land use data (whether public or private). Appropriate examples include:
- ISO 19115 (geospatial metadata standard)
- DCAT-2 (Data Catalog Vocabulary, version 2)
- The Dublin Core (DCMI)

### Compatibility and re-use

Compatibility with existing New Zealand classification systems shall be preferred in the design of classification systems. It shall take the form of published concordances where such associations are possible. Examples of re-use and compatibility include PAN-NZ for conservation land; ANZLIC for industrial categories; and Dairy NZ classes.

This concept extends beyond land use narrowly considered, and extends to land use management practices and lists of commodities, i.e. established vocabularies. For example, we encourage application of the [New Zealand Farm Data Standards](https://www.datalinker.org) glossaries.

### Definition of land

Classification systems shall individually determine the definition of "land". In particular, to what extent it includes marine and terrestrial water bodies.

This is also relevant for land use classification systems to declare their appropriate extent of application. For example, whether a land use classification system should be applied to New Zealand's offshore islands, marine areas (out to the EEZ), the entire continental shelf, etc. There is no consensus that a definition of "land" can exclude uses such as aquaculture, marine conservation areas, fishing areas, mining permits, shipping lanes, etc., particularly in the notable absence of "sea use maps".

This also allows for classification systems that are developed for particular application to the _rohe pōtae_ of iwi but may be inappropriate elsewhere.

### Primary land use

Some classification systems are intended only to capture "primary" land use for geographic entities, typically defined in economic terms. Some classification systems allow for the encoding of multiple uses, but in such a way that information about the primary land use is lost. (For example, the _ratings valuation rules_, LINZ S30300, allow for "multiple use" classes without the ability to encode the component uses.)

Data schemas for land use classification systems produced under this framework shall be designed in such a way that multiple uses can be recorded, without loss of information. This may be as a primary/secondary distinction, an enumeration, or some other form of attribution; but it must be possible in some fashion.

### Provenance

The value of land use data is enhanced when information is available regarding provenance. This relates to the epistemological foundation of land use data: how it is that we know the land use. Within the data schema of a classification system, it must be possible to record provenance information, including (but not limited to) if applicable:
    - the geographic scale of any input data
    - the publication or (preferably) feature-level creation date of any input data features
    - the operator (who is performing the classification; or who has decided on the appropriateness of a particular class label for a feature)
    - a quantitative (e.g. probabilistic) or qualitative (e.g. operator confidence) measurement of confidence in the applied class



---

## Contribution

TBD 

<!-- Workshops -->

<!-- Some procedure for contributing to this framework itself  -->

--

<!-- ## Matrix framework

Following [[2]](#2)

| Dimension used in classification| Individual or group information - extended family (Whānau) or individual (highly sensitive or personal information) | Māori databases such as the iwi or hapū tribal level (secured protection of information) | Regional and district databases, such as local government (conditions and criteria required for storing confidential information) | National level, central government (national databases, public domain access) |
|:---|:---|:---|:---|:---|
| Flora and Funga | Plant uses, plant varieties, medicinal plants, plants for weaving etc. | Local information on vegetation types | Regional or district data on vegetation and land use | National or regional data on vegetation (land cover) |
| Fauna | Special fauna, such as special foods, cultural arvest, fishing grounds, etc. | Local information on fauna | Regional or district data on fauna | National or regional data on fauna |
| Land, soil | Special landmarks, land features, traditional knowledge on soils and cultivation, muds/dyes for weaving, etc. | Tribal information on land features, landforms, soils, etc. | Regional or district data on landforms, soils, etc. | National or regional data on landfrosm, soils etc. |
| Water | Detailed or confidential information on water | Tribal information on water | Regional or district data on water | National or regional data on water |
| Air | Detailed or confidential information on air | Tribal information on air | Regional or district data on air | National or regional data on air |
| Special places | Detailed or confidential information on special places, cultural and historic sites | Tribal information on special places, cultural and historic sites (such as archaelogical sites) | Regional and district information on special places, cultural and historic sites | Limited information on special places, cultural sites |
| Sacred sites | Detailed or confidential information on sacred sites (e.g. burial grounds) | Tribal information on sacred sites | Regional and district information on some sacred sites (generalised information) | (Little or no information at this scale) |
| Metaphyiscal | Detailed or confidentail metaphysical information (such as spiritual, cosmological) | Tribal information on metaphysical information | (No information at this scale) | (Little or no information at this scale) |

--- -->

## Glossary

[Link](docs/Definitions_KeyConcepts-table.md)

---

<!-- Normative -->

## Land Use Classification Systems

This is a list of land use classification systems that are (being) developed under this classification framework. 

| Name | Link | Intended purpose |
|------|------|------|
| NZ Land Use Management and Tenure | [🔗](classification-systems/nzlumt/nzlumt.md) | General rural land use change monitoring, especially for freshwater monitoring and greenfield development |

<!-- ![a worked example](figs/Framework-Classification-02.png)
Fig N. a worked example... -->

## References

[^1] Denham, R. (2005). Accuracy assessment for land use mapping. Queensland Department of Natural Resources and Mines, Brisbane, and the Bureau of Rural Sciences, Canberra.

[^2]: Statistics New Zealand, Ministry for the Environment, Department of Conservation (2013). Environment domain plan 2013: Initiatives to address our environmental information needs. Available from www.stats.govt.nz

<!-- <a id="2">[2]</a>
Harmsworth, G. (1999).
Indigenous values and GIS: a method and a framework.
Business Alert 14.1 (1999): 10-15. -->

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
