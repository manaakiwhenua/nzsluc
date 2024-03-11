# NZSLUC

**THIS IS AN UNPUBLISHED AND UNREVIEWED DRAFT**

[![manaakiwhenua-standards](https://github.com/manaakiwhenua/nzsluc/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

<!-- TODO some sort of foreword; why we are making this -->

Land use information is needed to respond to New Zealand's environmental, social and economic challenges, including water quality, soil erosion, natural disaster planning and response, and greenfield development.

# The New Zealand Standard Land Use Classification Framework

The NZSLUC Framework presents principles, procedures and definitions for designing compliant land use classification systems. 

<!-- Informative -->
## Principles

1. To support the production of **nationally consistent** data on land use
2. To suppot classification systems that classify land at the **parcel level or beyond**. <!-- More explicit scale? Raster/DGGS resolution? Landscape objects? -->
3. To facilitate the production of **consistent land use information** in New Zealand, such as from regional government agencies.
4. To facilitate the use of land use data at national, regional and local scales.
5. To incorporate land management practices when needed to distinguish between land uses.
6. To **propose** NZSLUC classifications that are intended to be revised in a series of reviews with partners and stakeholders
    - It is particularly important that **iwi/Māori partners** are involved throughout.
<!-- - To achieve national understanding before releasing the data adhering to a proposed classification system. -->
7. To support the development and implementation of **more than one classification system** under this framework _and_ to ensure that they are broadly compatible. <!-- Compatible = weasly? -->
8. To balance **reliability, practicality, and cost effectiveness** in the production of land use data artefacts.
9. To adhere to specifications for land use classfications including:
    - To attribute of the prime land use
    - To facilitate attribution of secondary or mixed uses
    - To record source information (i.e. provenance: geographic scale, date, and confidence)
    - To be able to record commodities from a set of standard codes (e.g. DataLinker, Stats NZ)
    - To be able to record management practices from a set of standard codes (to be determined)
    <!-- - Tenure -->
10. To aspire to ensure **overall attribute accuracy of greater than 80 per cent**.
11. To carefully develop these principles, proceedures, definitions and classification systems themselves over time, with concern for backwards compatibility.
12. To require allowing multiple land uses to be represented
13. To require allowing land use classification systems to be multidimensional (ref. Rutledge) <!-- Semantic? -->
<!-- - To allow the incorportation of multiple dimensions of land use -->
<!-- - To require that participating land use classifications are multidimensional in operation -->
<!-- - Dimensions
    - Commodities
    - Management practices
    - Tenure -->

<!-- Principles for reuse -->
<!-- Principles for contribution -->
<!-- Principles for systematic classification -->
<!-- Principles for publishing data artefacts -->

## Procedures 

<!-- Mutlidimensional? What dimensions? -->
<!-- Proceedure for reporting land use change? -->
- Recommended that published data is independently validated, and quality is described using a standard such as xyz
- One or more established metadata standards shall be used when publishing data
<!-- LUML? -->
<!-- Compatibility with other classification systems in components, e.g. PAN-NZ, ANZLIC for industrial categories, Dairy NZ classes, etc.? -->
<!-- What is the extent? Marine? What is "land"? EEZ, etc. -->

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



## Definitions / Key Concepts

| Concept | Description | Reference(s) |
|---------|:-----------:|-------------:|
| Land use | The purpose to which land is committed. | ... |
| Tenure | The form of an interest in land. | ... |
| Commodity | A product. | ... |
| Management practice | A practice. | ... |

---

<!-- Normative -->
# The New Zealand Standard Land Use Classification Systems

Lorem ipsum
<!-- All spatial data/metadata will adhere to OGC/ISO standards -->
<!-- Hierarchical classification like so... -->

---

## Current land use mapping in New Zealand

<!-- TODO refer to a separate Markdown summary, or report section -->

## References
<a id="1">[1]</a>
Denham, R. (2005).
Accuracy assessment for land use mapping.
Queensland Department of Natural Resources and Mines, Brisbane, and the Bureau of Rural Sciences, Canberra.