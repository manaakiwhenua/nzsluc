# NZSLUC

**THIS IS AN UNPUBLISHED AND UNREVIEWED DRAFT**

[![manaakiwhenua-standards](https://github.com/manaakiwhenua/nzsluc/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

<!-- taken directly from contract; first para -->
New Zealand currently lacks a comprehensive **, cohesive** land use information system. There is a lack of consistent definition or approach to mapping land use at the national and regional levels. Understanding land use consistently across New Zealand and over time would enable us to better understand the impacts of land use on ecosystem services, support the modelling of the impacts of climate change, and help profile natural disaster risks among other benefits.

<!-- Standardised land use information is needed to respond to New Zealand's environmental, cultural, social and economic challenges, including water quality, soil erosion, natural disaster planning and response, greenfield development, and more holistic concerns. -->

A litany of land use classifications have been developed for New Zealand, primarily drawing on the same (or very similar) public and commercial data. Few, if any, having been more widely adopted. One of the primary reasons for this outcome being each system is quite narrowly focused and uses data tightly coupled to that specific classification and/or application, without consideration of a broader perspective or context.

We propose any New Zealand land use classification adhere to common principles, or a common framework, such that the objects being considered in the classification carry the same meaning across any instantiated output.  This document is an initial draft of such a framework. 

A land use classification _framework_ should include principles appropriate for any land use classification system (or output---i.e. a map) while remaining flexible enough to facilitate all relevant use-cases illustrating the requirement of a specific need or value (e.g. a _type_ of land use).  This may include hierarchies for generalization as well as other types of relational information such as lineage, parts, terminological variation,....
This is important as it will facilitate 1 to 1, 1 to many, many to 1, and many to many relationships as they are appropriate, even if all that can be captured is that there _is a_ relation between two entities despite not fully understanding how the entites may be related --- e.g `skos:related`.

The **land use classification _framework_** should consider over-arching principles and purposes~~, roles, principles, and procedures~~ for any land use classification _system_. It should not be overly prescriptive, allowing for multiple classification systems to co-exist—provided they adhere to the framework principles.

**Land use classification _systems_** should be developed within this framework. It is at this level that a more concrete system of classes may be created. It is unlikely that one classification _system_ will be appropriate for all data or use cases. The intention is for multiple systems to be developed for a variety of purposes using a variety of properties, potentially only available at specific, and limited, spatial or temporal scales.

For example, it may or may not be appropriate for any given system to incorporate a hierarchical structure, either as a generalization or genealogy (e.g. lineage). While this particular notion may specific to a land use classification system, the land use classification framework should allow for either, or both.  

# The New Zealand Standard Land Use Classification Framework

The NZSLUC Framework presents principles, procedures and definitions for designing land use classification systems. Classification systems that adhere to this framework are considered to be _compliant_ with the classification framework.

## Principles <!-- Informative -->
1. #### Prioritize Data
1. #### Specificity
    each classification is designed for an intended spatiotemporal geographic unit  
1. #### Hierarchies are encouraged where appropriate
    1. generalization hierarchy (aggregation/disaggregation) 
    1. genealogical hierarcy (lineage) 
1. #### Primary use, ancillary use, and system variablity
1. #### This classification framework is fallible
    The classification framework shall be modified (improved?) at regular intervals based on comments and requests of any/all stakeholders (e.g. a development cycle)


_____________________________________________________________________________________
1. To support classifications systems that work at a variety of geographic scales.
1. To encourage multidimensional conceptualisations of land use, with particular regard for the following dimensions:
    - Commodities
    - Management practices
    - Tenure

1. To continually revise these principles, and any derived classification systems
    - with partners and stakeholders, especially iwi/Māori partners
    - with concern for backwards compatibility and the recording of change over time


1. To support the production of nationally consistent data on land use
    - through careful selection of these principles
    - through careful specification of required procedures
1. To balance **reliability, practicality, and cost effectiveness** when determining procedures.

## Procedures <!-- Normative -->

The brief list of procedures for land use classification systems under this framework is below. Following subsections add detail.

1. **Validation** Published data shall be independently validated, and quality described using a standard. Overall attribute accuracy of 80% shall be adopted as a minimum standard.
1. **Semantic versioning** Changes made to land use classification systems shall be communicated to users using semantic versioning of the form `major.minor.patch`, e.g. v0.2.4. Once a version has been release, the contents of that version must not be modified; modifications must be released as a new version.
    - Major version for backwards incompatible functionality.
        - Major version 0 is reserved for initial development and tolerance for change is higher than for other major versions.
    - Minor version for new or modified functionality in a backwardly compatible manner.
    - Patch version for backwardly compatible fixes and minor adjustments.
1. **Publication and metadata** Land use datasets shall be maintained on data repositories, and published with standardised metadata.
1. **Stability of geographic scale** Geographic scales and entities are to be considered stable.
1. **The effect of ISO 19144-3** The publication of the ISO 19144-3 standard (_Geographic information – Classification Systems – Part 3 Land Use Meta Language (LUML)_) shall cause a revision of these procedures. This standard is likely to affect the appropriate procedures for land use classification systems.
1. **Compatibility with existing land use classification systems** Compatibility with existing New Zealand classification systems shall be considered. Compatibility with international classification systems may also be relevant.
1. **Definition of land** Classification systems shall individually determine the definition of "land" with reference to their stated purpose.
1. **Mixed and secondary uses** Classification systems shall ensure that mixed or secondary uses may be attributed to land.
1. **Provenance** Source information (i.e. provenance, geographic scale, date, operator, and confidence) shall be recorded.
<!-- Classification systems shall use vocabularies that are available (normatively) as RDF, accessible via SPARQL 1.1 endpoints. -->
<!-- Some procedure for contributing to this framework itself  -->
<!-- Some Ppocedure regarding the standardisation of regional input data? -->

![a worked example](figs/Framework-Classification-01.png)
Fig N. Overview figure.

### Validation

A land use product should not be considered complete until an accuracy assessment has been conducted. Errors can be thematic or spatial, and these errors are not independent. Validation should be reported as a confusion matrix of classification classes, such that users can determine that a geographic unit mapped as class _i_ is class _j_ on the ground for any class _i, j_. This assessment requires that a number of known units are compared to their classified values. This assessment should be made on the basis of ground-truth, local knowledge, and aerial imagery (in descending preference order) and shall not be conducted by those involved in the classification proceedure itself.

Recommended procedure (based on ALUM):
1. Determine which classes can be validated. Not all classes in a classification system are assessable. Justifications for excluding a class from validation include:
    1. If land use can only be determined based on tenure rather than physical attributes (typical examples: forms of conservation land; water supply areas)
2. Conduct a stratified random sample strategy should be conducted, using the map classes as the strata; the sample size within each stratum is in proportion to the occurrence of that class in the land use product. The total sample size shall be limited to a fixed number of total assessments (e.g. 1,000). In practice, the sample may be larger; it should increase with the number of classes within the classification system, the number of available validators, and the size of the intended audience.
3. The assessment unit is the same as the geographic unit, e.g. a parcel or cell.
4. Construct an error matrix, comparing land use classes for sampled geographic units with the observed land use classes. Compute the total, user's and producer's accuracies for the map. Also compute 90% confidence intervals for each estimate. (See [[1]](#1).)
5. Determine if the map meets the required level of accuracy. If the _lower bound_ of the confidence interval for total accuracy is greater than this level (**80%**), then the map meets the framework specification. If any of the upper bounds of the user's or producer's accuracies is less than 50%, then the map may also be considered to have failed the specification, however there may be some scope for judgement in certain classes due to unavoidable confusion between similar classes. If validation fails, perform a re-classification focussed on addressing the worst-performing classes, and repeat the validation proceedure for all clases.
6. Report the accuracy, including the error matrix and a map of sample sites.

It is recommended that validation results are made available, conforming to the ISO 19157-1:2023 (Geographic information — Data quality) standard.

### Semantic versioning

### Publication and metadata

Published land use data shall be made available on public data repositories. Exceptions to this may be made for land use classifications with information considered sensitive by those supplying data or interpretative information. However, making data available on a data repositories with privacy controls is still recommended.

One or more established metadata standards shall be used when publishing land use data (whether public or private):

- The Dublin Core (DCMI)
- DCAT-2 (Data Catalog Vocabulary)
- ISO 19115 (geospatial metadata standard)

### Stability of geographic scale

Geographic units and geographic scales form an intrinsic part of the specification of a land use classification system, and changes to these are to be considered _major_ version changes to a classification system. The reason for this is that stability in the geographic frame of reference is critical to support analysis of land use change over time.

### The effect of ISO 19144-3

### Compatibility with existing land use classification systems

Compatibility with existing New Zealand classification systems (PAN-NZ for conservation land; ANZLIC for industrial categories; Dairy NZ classes; etc.) shall be considered in the design of classification systems. It shall take the form of published concordances where such associations are possible.

It may also take the form of using an existing classification system within a wider land use classification system; for instance, using PAN-NZ as a classification sub-system for classifying land that is statutorily protected.

This concept extends beyond land use narrowly considered, and extends to land use management practices and lists of commodities. For example, we encourage application of the [New Zealand Farm Data Standards](https://www.datalinker.org) glossaries. 

### Definition of land

Classification systems shall individually determine the definition of "land".

In particular, to what extent it includes marine and terrestrial water bodies.

This is also relevant for land use classification systems to declare their appropriate extent of application. For example, whether a land use classification system should be applied to New Zealand's offshore islands, marine areas (out to the EEZ), the entire continental shelf, etc. There is no consensus that a definition of "land" can exclude uses such as aquaculture, marine conservation areas, fishing areas, mining permits, shipping lanes, etc., particularly in the notable absence of "sea use maps".

This also allows for classification systems that are developed for particular application to the _rohe pōtae_ of iwi but may be inappropriate elsewhere.

<!-- copied directly from Cavanagh and Whitehead 2023 -->
‘Land use’, ‘land cover’ and ‘land management’ are often used interchangeably in discussions about land use. This erroneous use seems to largely stem from a lack of awareness of the distinct meaning of each of these terms.  The following definitions, which have been drawn from the [Australian Department of Agriculture, Water and the Environment](https://www.awe.gov.au/abares/aclump/definitions), help to make explicit the differences. 
- Land use means the purpose to which the land is committed, including the production of goods (such as crops, timber, and manufactures) and services (such as defence, recreation, biodiversity, and natural resources protection)
- Land management practice means the approach taken to achieve a land-use outcome – the 'how' of land use (e.g., cultivation practices such as minimum tillage, direct drilling, and choices around stocking rate density). 
- Land cover refers to the physical surface of the earth, including various combinations of vegetation types, natural bare surfaces (e.g., exposed rock or gravel, permanent snow and ice, etc.), and water bodies as well as anthropogenic elements, such as agriculture, transport infrastructure and built environments. Land-cover classes can usually be distinguished by characteristic patterns using remote sensing. 
- Land-use classification provides general information on land cover, and the types of human activity involved in land management.  
<!-- end copy -->

### Mixed and secondary uses

Some classification systems are intended only to capture "primary" land use for geographic entities, typically defined in economic terms. Some classification systems allow for the encoding of multiple uses, but in such a way that information about the primary land use is lost. (For example, the _ratings valuation rules_, LINZ S30300, allow for "multiple use" classes without the ability to encode the component uses.)

Data schemas for land use classification systems produced under this framework shall be designed in such a way that multiple uses can be recorded, without loss of information. This may be as a primary/secondary distinction, an enumeration, or some other form of attribution; but it must be possible in some fashion. 

### Provenance

The value of land use data is enhanced when information is available regarding provenance. This relates to the epistemological foundation of land use data: how it is that we know the land use. Within the data schema of a classification system, it must be possible to record provenance information, including (but not limited to) if applicable:
    - the geographic scale of any input data
    - the publication or (preferably) feature-level creation date of any input data features
    - the operator (who is performing the classification; or who has decided on the appropriateness of a particular class label for a feature)
    - a quantitative (e.g. probabilistic) or qualitative (e.g. operator confidence) measurement of confidence in the applied class

---

## Definitions / Key Concepts

| Concept | Description | Reference(s) |
|---------|:-----------:|-------------:|
| Land use | The purpose to which land is committed. | ... |
| Tenure | The form of an interest in land. | ... |
| Commodity | A product. | ... |
| Management practice | A practice. | ... |

---

<!-- Normative -->

# Land Use Classification Systems

This is a list of land use classification systems that are (being) developed under this classification framework. 

| Name | Link | Intended purpose |
|------|------|------|
| TBD  | [🔗](classification-systems/nzslucs.md) | General environmental change, especially for freshwater monitoring and greenfield development |


![a worked example](figs/Framework-Classification-02.png)
Fig N. a worked example...

# References
<a id="1">[1]</a>
Denham, R. (2005).
Accuracy assessment for land use mapping.
Queensland Department of Natural Resources and Mines, Brisbane, and the Bureau of Rural Sciences, Canberra.
