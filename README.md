# NZSLUC

[![CC BY 4.0][cc-by-shield]][cc-by]

[![manaakiwhenua-standards](https://github.com/manaakiwhenua/nzsluc/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

New Zealand currently lacks a comprehensive and cohesive land use information system. There is a lack of consistent definition or approach to mapping land use. Consistent land use information for New Zealand (over space and time) would improve the understanding of the implications of land use across social, cultural, economic and environmental domains.

Many land use classifications have been developed for New Zealand, primarily drawing on the same (or very similar) public and commercial data. Few, if any, having been re-used. One of the common reasons for this outcome is that systems tend to narrowly focus and use data that is tightly coupled to one specific application.

We propose that any New Zealand land use classification system adheres to common principles in a common framework.

We propose a **land-use classification _framework_**  that includes principles and best practices appropriate for any land-use classification system (and associated output; i.e. geospatial information and maps). This must allow for multiple land-use classifications systems, each with its own intended use cases, potentially across multiple value systems. This may (or may not) include hierarchies for generalisation, as well as other types of relational information, such as lineage, parts, and/or terminological variation. Multiple hierarchies are important because they will facilitate one to one, one to many, many to one, and many to many relationships, as appropriate, even if all that can be captured is that there is a relation between two classes, despite not fully understanding how the classes are related.  <!--  --- e.g `skos:related`. -->

We also propose that **land use classification _systems_** be developed within the proposed framework. It is at the classification system level that a more concrete set of classes can be designed. It is unlikely that one classification system will be appropriate for integrating all data or for application in all use cases. The separation of concerns between the framework and the system allows for the development of multiple systems using a variety of properties, potentially only applicable at specific spatial or temporal scales, limited extents, or specific purposes (including for the purposes of confidentiality and indigenous data sovereignty). 

# The New Zealand Standard Land Use Classification framework (NZSLUC)

The NZSLUC framework presents principles and best practices for designing land-use classification systems. Principles are intended to guide practitioners in how they use, reuse or design classification systems. 

> **Kua raranga tahi tatou he whāriki, mātauranga mō āpōpō.**
> 
> _Together we weave the mat / In terms of [mātauranga](https://maoridictionary.co.nz/word/3830) / For future generations._

This [whakataukī](https://maoridictionary.co.nz/word/9903) envisions a mat-weaving analogy, which in this context recalls the reliance on multiple independent sources of input data, information, and knowledge from different people and organisations, with the ultimate aim of creating a shared understanding of land use as spatial information. A land-use map can be used by and for future generations to answer the enduring questions they have about land. 

## Principles <!-- Informative -->

1. #### Prioritise atomic data (i.e. the decomposition of multi-dimensional attributes to observable, discrete characteristics; e.g. tenure). 
    - Classification systems should break down information being collected into individual (atomic, primitive, indivisible, discrete) attributes (diagnostic criteria) to expose important data-differentiating categories. 
    - Classification systems should be based on collections of primary data (rather than secondary categorial data), where feasible. 
1. #### Be specific about purpose and scope.
    - Classification systems shall be designed for an explicit spatiotemporal geographical unit (e.g. property parcels with land use recorded over a seasonal time scale). 
    - Classification systems should consider the additional use of abstract fixed geographical units, such as DGGS zones, so that data can be reorganised to different geographical units. 
    - Classification systems do not have to be comprehensive and will almost certainly consider some land-use types ‘out of scope’, according to the purpose. 
1. #### Ensure extensibility.
    - Classification systems shall ensure flexibility for land-use classification systems that support indigenous data sovereignty protocols (see [Te Mana Raraunga – Māori Data Sovereignty Network](https://www.temanararaunga.maori.nz/)). 
1. #### Use hierarchies where they are appropriate, required, and logically consistent.
    - Classification systems should consider the possibility for both generalisation hierarchies (aggregation/disaggregation) and genealogical hierarchies (lineage).
1. #### Improve over time.
    - The classification framework itself shall be reviewed based on the comments and requests of stakeholders. 
    - The publication of the ISO 19144-3 standard (Geographic information – Classification Systems – Part 3 Land Use Meta Language (LUML)) shall prompt an examination of these principles and best practices. 
1. #### Prioritise reproducible and transparent methodologies 
    - Classification systems should allow for their methodology to be independently verified.
1. #### Accommodate multiple land uses.
    - Classification systems should differentiate between secondary/co-located land uses (same place, same time) with intra-period land-use variation (same place, different time); e.g. rotational grazing, summer housing. 

## Best practices <!-- Normative -->

This collection of best practices is intended for producers of land-use information to benefit the consumers of land-use information.

The list of best practices for land use classification systems under this framework is below.

<!-- 1. Data product specification, e.g. ISO 19131:2022 -->
1. **Purpose** Land use classification systems shall describe their intended use-cases.
1. **Scope** Land use classification systems shall describe their intended scope.
1. **Extensibility** Ensure flexibility for land use classification systems to interact with other land use data and classification systems. This must include, for example, Māori attribute layers that maintain indigenous data sovereignty.
1. **Description of data quality** The quality of published land use data shall be described using a standard, e.g. ISO 19157-1:2023.
1. **Semantic versioning** Changes made to land use classification systems (including geographic unit or scale) shall be communicated to users using semantic versioning of the form `major.minor.patch`, e.g. v0.2.4. Once a version has been released, the contents of that version must not be modified; modifications must be released as a new version.
1. **Metadata** Land use datasets and classification schema should be published using established metadata standards.
1. **Compatibility and re-use** Compatibility with existing New Zealand classification systems shall be preferred. Compatibility with international classification systems may also be relevant.
1. **Definition of land** Classification systems shall individually determine the definition of "land" with reference to their stated purpose, e.g. whether it is inclusive of marine features.
1. **Primary land use** A justification should be given for the choice of primary land uses (e.g. land area, economic value, duration).
1. **Provenance** Source information (i.e. geographic scale, time/date, operator, and confidence) shall be recorded.


<!-- ![a worked example](figs/Framework-Classification-01.png)
Fig N. Overview figure. -->

### Purpose

Land-use information is collected at multiple scales and for a variety of purposes, which, directly and indirectly, affect relevant decisions based on how that information is organised and/or applied. It is best practice to explicitly state the purpose for which land-use classification systems are designed, and this purpose will inform other decisions. When deciding on the purpose, consider what questions are likely to be answered if land-use information is systematically organised according to the classification system. An inter-agency central government report provides a useful framing for these questions as ‘enduring’; i.e. questions that do not really change over time, but the way we answer them (under a type of system or architecture) does (Stats NZ et al. 2013)[^1].

Choice of geographical unit (e.g. property parcels) may make extension and reorganisation of land-use information difficult in some circumstances. Obviously there are pragmatic reasons for choices of this nature. Be mindful of knock-on effects stemming from what are effectively modelling decisions. Potential issues include alignment with existing tools or published data, computational (in)feasibility, the expected absence of finer-scale input data, restrictions on the use of required input data, and privacy. Where possible, a specification to use grids without pre-defined boundaries (such as [DGGS zones](https://docs.ogc.org/as/20-040r3/20-040r3.html) or raster grids) should be preferred. 

### Scope

Land-use classification systems should describe their intended scope (e.g. spatiotemporal characteristics) and domain of discourse. Land-use classification systems need not be comprehensive: they may consider only a few land-use types and deem others as ‘out of scope’. For example, a classification of protected land may choose to classify all other land as non-protected without attempting more precise classification, according to the purpose of that classification system.

### Extensibility

Ensure flexibility for land-use classification systems to interact with other land-use data and classification systems. This must include, for example, Māori attribute layers that maintain indigenous data sovereignty. 

It should always be possible to extend or widen a classification system with more properties/attributes that can be determined by other users, such that information can be reorganised, re-presented, and corrected according to local priorities, and owned by individuals, hapū, and iwi without an expectation that this will be visible ‘upstream’.  

Allowing both a class hierarchy and the annotation of multiple attributes is intended to enable the representation of whakapapa (genealogy) and whanaungatanga (origins, interdependencies, and interconnections) within a land-use classification system; and to represent the multiplicity of uses any area of land can simultaneously be associated with, which may go beyond the original intended purpose of a land-use classification system.

### Data quality

The quality of published land-use data should be described using a standard (e.g. ISO 19157-1:2023).

### Semantic versioning

Any changes made to already-published land-use classification systems (including changes to the geographical unit or geographical scale) should be communicated to users using semantic versioning indicating major, minor and patch versions, e.g. v0.2.4. Once a version has been released, the contents of that version must not be modified; modifications should be released as an updated version.

The following are guidelines for semantic versioning:

- Major version for backwards incompatible functionality.
    - Major version 0 is reserved for initial development and the tolerance for breaking change is higher than for other major versions.
- Minor version for new or modified functionality in a backwardly compatible manner.
- Patch version for backwardly compatible fixes and minor adjustments.

### Metadata

One or more established metadata standards should be used when publishing land-use data (whether public or private). Appropriate examples include:

- ISO 19115 (geospatial metadata standard)
- Dublin Core (DCMI)
- DCAT-2 (Data Catalog Vocabulary, version 2)
- Schema.org

### Compatibility and reuse

Compatibility with existing New Zealand or international classification systems should be preferred in the design of classification systems. This should take the form of published concordances where such associations are possible. Examples of reuse and compatibility include Protected Areas Network of New Zealand (PAN-NZ) for conservation land, Australia and New Zealand Land Information Council (ANZLIC)for industrial categories, and DairyNZ classes. 

This concept extends beyond land use narrowly considered and extends to land-use management practices and lists of commodities (i.e. established vocabularies). As an example, consider the [New Zealand Farm Data Standards](https://www.datalinker.org) glossaries. 

### Definition of land

Classification systems should individually determine the definition of ‘land’ with reference to their stated purpose (e.g. whether it includes marine and terrestrial water bodies). It is also relevant for land-use classification systems to declare their extent of application (e.g. whether it should be applied to New Zealand's offshore islands, marine areas out to the Exclusive Economic Zone, the entire continental shelf, etc). There is no consensus as to whether a definition of ‘land’ can exclude uses such as aquaculture, marine conservation areas, fishing areas, mining permits, shipping lanes, etc., particularly in the notable absence of sea-use maps. This also allows for classification systems that are developed for particular application to the rohe pōtae (tribal territory) of iwi, but it may be inappropriate to apply elsewhere.

### Primary land use

A justification should be given for the choice of primary land uses (e.g. land area, economic value, duration). Some classification systems are intended to capture only the primary land use for geographical entities, typically defined in economic terms. Some classification systems allow for the encoding of multiple uses, but in such a way that information about the primary land use is lost. For example, the ratings valuation rules ([LINZS30300](https://www.linz.govt.nz/resources/regulatory/rating-valuations-rules-2008-version-date-1-october-2010-linzs30300)) allow for ‘multiple use’ classes without the ability to encode the component uses.

In contrast, data schemas for land-use classification systems produced under this framework should be designed in such a way that multiple uses can be recorded without loss of information (as with indeterminate ‘mixed’ classes, where the components are unspecified). This may be as a primary/secondary distinction, an enumeration, or some other form of attribution, but it must be possible in some fashion.

### Provenance

Source information (i.e. geographical scale, time/date, operator, and confidence) should be recorded. The value of land-use data is enhanced when information on provenance is available. This relates to the epistemological foundation of land-use data: how it is that we know the land use? Within the data schema of a classification system it must be possible to record provenance information, including, if applicable:

- the geographical scale of any input data
- the publication or (preferably) feature-level creation date of any input data features
- the operator (who is performing the classification or who has decided on the appropriateness of a particular class label for a feature)
- a quantitative measurement (e.g. probabilistic) or qualitative statement (e.g. operator confidence) of confidence in the applied class.

---

## Contribution

TBD

## Glossary

[Link](docs/Definitions_KeyConcepts-table.md)

---

## Land Use Classification Systems

This is a list of land use classification systems that are (being) developed under this classification framework. 

| Name | Link | Intended purpose |
|------|------|------|
| NZ Land Use Management | [🔗](classification-systems/nzlum) | General rural land use change monitoring, especially for freshwater monitoring and greenfield development |

<!-- ![a worked example](figs/Framework-Classification-02.png)
Fig N. a worked example... -->

## References

[^1]: Statistics New Zealand, Ministry for the Environment, Department of Conservation (2013). Environment domain plan 2013: Initiatives to address our environmental information needs. Available from www.stats.govt.nz

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
