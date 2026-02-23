# New Zealand Land Use Management (NZLUM) classification system 

> [!IMPORTANT]  
> This repository contains a SKOS concept scheme for the NZLUM land-use classification (`nzlum.ttl`) and a SHACL shapes file (`shapes.ttl`) used to validate required fields and hierarchy consistency.
>
> Future vesions of this classification will be maintained as a versioned SKOS concept schema. Human-oriented lists of classes with definitions will be generated from this. This is a work-in-progress, beginning with the class schema.

>[!NOTE]
> This will be controlled with GNU Make:
> ```bash
> make build/nzlum-{version}.ttl
> make shacl
> make tables-all
> make outline-all
> ```

NZLUM is adapted from the Australian Land Use and Management (ALUM) classification (version 8) for application in New Zealand, taking into account common land-use classification usage in New Zealand for several different purposes, including SOE soil quality monitoring (see Cavanagh & Whitehead 2022, 2023)[^1][^2], the Waikato Integrated Scenario Explorer (Rutledge et al. 2016)[^3], Greater Wellington Regional Council whaitua (catchment) classifications (Cavanagh 2022), Land Use Database version 4 (LUDB4) (Price et al. 2010)[^4], the New Zealand Planning Standards (MfE 2019)[^5], and LINZ rating valuations rules (LINZ 2010) [^6].

The rationale for the adaptation of ALUM is that ALUM provides a useful data structure and platform for standardisation, which, simply put, avoids some reinvention of the wheel in this regard. ALUM is licensed under a [Creative Commons Attribution 3.0 Australia Licence](https://creativecommons.org/licenses/by/3.0/au), which explicitly permits adaptation of ALUM. Where direct overlap of an ALUM class is considered appropriate, it has been retained. However, both particular classes and the arrangement of the class hierarchy are significantly different, and additional classes have been added to reflect what we consider to be relevant considerations for land-use information in New Zealand.

The two biggest changes from ALUM are the removal of consideration of irrigation as a demarcation between two primary classes of agriculture, and the removal of water as a primary class. We considered ALUM’s division and duplication of classes according to irrigation status to be redundant, given that irrigation (status and type) can be recorded as a management practice, and that retaining it would impede usability. We also modified the primary intensive-use class to separate intensive agricultural production from other intensive land uses and included these within the primary agricultural production class.

The other major difference is the absence in NZLUM of a water primary class. We have done this not because we consider water unimportant or out of scope, but rather because we consider water to be a land cover, not a land use. We propose an attribute to capture the presence of water using a controlled vocabulary of terms for water features (such as `river`). In this way, end-users can control the inclusion or exclusion of water features.

Certain land uses can only occur on water (e.g. aquaculture and fisheries); some can occur on either land or water (e.g. oil and gas infrastructure), or at the interface of land and water (ports and wharves); and obviously many land uses can only occur on land (e.g. pastoral farming), but, even then, pieces of such land may include water (e.g. dams, ponds, and lakes), or affect water (irrigation water take consents, tailings, and pollution). ALUM classifies water as a primary class but admits that this presents some difficulty. One proposal for NZLUM is that water be recorded as a distinct attribute that can be applied to a geographical unit.

Currently there is inconsistency in our proposal with respect to how water features should be captured; see, for instance the water features under class 2 (Production agriculture and plantations) and class 3 (Built environment). This inconsistency should be resolved before applying this draft classification system, because a final decision about the treatment of water will affect future organisational changes to the classification system. Water also has a special status for Māori, and engagement with iwi/Māori in the further development of this classification system is required. Here we do make the case that including water as a land cover attribute, rather than a class, does have merit.

Following the pattern of ALUM attributes (for commodities and management practices), we propose that a water attribute should have an associated, controlled set of terms that could be applied to a geographical unit. An incomplete short list (using English language terminology) is:

- `lake`
- `reservoir`
- `dam`
- `evaporation basin`
- `river`
- `channel`
- `aqueduct`
- `wetland`
- `estuary`
- `intertidal`
- `marine`

Subtypes could be used to disambiguate where information allows. For example, just as the list of commodities allows for either `cattle` (i.e. unspecified) and `cattle dairy`, `cattle beef`, `cattle meat` to accommodate some additional information, one could imagine the use of `marine inshore`, `wetland stormwater`, and `wetland bog`. The parallel or exclusive use of te reo Māori terms could be helpful to create subtypes along dimensions that are important to Māori, and adds the potential for localism and flexibility on top of the classification system as it pertains to water. (Treating water as a primary class would not allow this to the same extent.)

Overall, this draft classification system is proposed as a ‘general purpose’ land-use classification in the context of grouping the nature of interaction of land-use activities with the use of soil and water resources relevant for land-use change modelling or environmental management. The development of the system will allow for some end-user reclassification of land use (e.g. on the basis of irrigated vs non-irrigated land to meet alternative purposes), although in other cases (e.g. for LUCAS LUM) and the specification of pre-1990 forest, or to better reflect te ao Māori values, additional classification systems would still more than likely be required.

The present classification system retains ALUM's practice of attempting to record additional information (e.g. land management practices) using defined terminology. The additional information – termed ‘attributes’ – is related to, but independent of, the land-use classes themselves.

The collection of specific additional attributes is intended to allow for the reclassification of land use based on these attributes, which may be able to be determined at the time of mapping, or recorded after the fact. The number and type of attributes captured within this system needs to be agreed in order to recognise the value of the information, and the context of use within this classification, versus the use of an alternative classification. These attributes are optional, but they should be included where information permits.

Potential attributes could include the following.

- **Commodities**  (as in ALUM): captures information about crops and livestock that allows for further distinction within a land-use class and may be useful in the context of biosecurity, economic modelling, nutrient modelling, greenhouse gas estimation, site-selection, etc.
- **Management practices** (as in ALUM): captures additional information not otherwise captured in the class hierarchy, such as irrigation, crop pasture rotations, free range stock, or wintering off of dairy stock. ALUM maintains a list of 44 management practices with agreed names (a controlled vocabulary, or enumeration – a set of named constants). This set of names was compiled from existing sources, such as the Australian Bureau of Statistics, Meat and Livestock Australia, Horticulture Innovation Australia, Grains Research and Development Corporation, and state and territory lists. NZLUM adoptis this list but allows some extensions. Management practices are expected to apply only to particular land-use codes, so they must be used in conjunction with stated codes.
- **Tenure**: relates to the potential for changes to land use and land-use management practices (because tenure may constrain possible land-use changes). Information relating to land tenure could be captured in two attributes: `land_estate` and `land_status`. How land is owned, and by whom, is an important consideration for how land may be used or managed. Recognising that tenure is an extension of the considerations of ALUM (on which this classification system is based), it is important to note that Boffa Miskell Limited (2023) identified the need for land tenure status as a requirement for a land information system to address the needs of councils to monitor and implement freshwater regulations, and to map urban growth.
- **Zoning**: such as that described in the 2019 New Zealand Planning Standards (e.g. rural zone, Māori purpose zone) will help to identify future land-use changes and can be matched with additional information such as land-cover information to confirm current use. Once again, the need for zoning information as a dimension of land information was identified in Boffa Miskell 2023; it is especially relevant for councils considering patterns of urban expansion and intensification.
- **Land cover**: this is particularly relevant in the context of identifying crop rotations within various primary production classes. These would probably be framed as land cover at the time of mapping. There would need to be further decisions regarding the appropriate land-cover terminology, so this idea has not progressed beyond an initial proposal.
- **Permeability**: whether land is considered ‘sealed’ or ‘unsealed’. This allows further delineation within classes, particularly in the built environment, which probably contains mixtures of sealed and unsealed land (e.g. in residential areas and road corridors).
- **Water**: as discussed above.

It is worth noting that all these attributes are categorial and not continuous variables. There may be a need to include additional continuous variables (such as farm stocking rates in stock units per hectare). However, these should be appropriately discretised or otherwise captured as ancillary information so that the total number of combinations of all attributes can be enumerated.

Land is classified according to its primary use, based on the primary land management objective of the landowner or manager, and additional ancillary land uses can be captured separately. Some uses may only ever be ancillary, so the proposed classification system necessarily includes some such uses.

An overview of the class hierarchy is available:

- As readable text: [nzlum_v0.4.0_outline.md](build/nzlum_v0.4.0_outline.md)
- As a table in text: [nzlum_v0.4.0.md](build/nzlum_v0.4.0.md)
- As a table in XLSX: [nzlum_v0.4.0.xlsx](build/nzlum_v0.4.0.xlsx)
- As RDF: [nzlum.ttl](build/nzlum-0.4.0.ttl)

## Data structure

This section specifies the proposed data structure for the attribution of land-use information. Each set of attributes applies to one geographical unit and can contain information about the primary and ancillary land uses, as well as attributes for disambiguation and end-user reclassification, recording provenance and any operator comments.

| attribute | type | example | notes |
| --- | --- | --- | --- |
| lu_code_primary | integer | `1` | Numerical land use code (primary use) at the primary level |
| lu_code_secondary | integer | `2` | Numerical land use code (primary use) at the secondary level |
| lu_code_tertiary | integer | `3` | Numerical land use code (primary use) at the tertiary level |
| lu_code | string | `1.2.3` | Complete land use code (primary use) |
| lu_description | string | `Natural Heritage` | Land use class label (primary use) |
| lu_code_ancillary | (sorted set of) string | `2.2.0,3.2.1` | Land use code (ancillary uses), multiple uses are to be specified with comma separation with optional whitespace characters |
| commod | (sorted set of) string | `cattle dairy` | Commodity type; multiple commodities are to be specified with comma separation with optional whitespace characters |
| commod_ancillary | (sorted set of) string | `pulpwood` | Commodity type(s) relating to the ancillary land use code(s) |
| manage | (sorted set of) string | `irrigation spray,organic` | Management practices; multiple practices are to be specified with comma separation with optional whitespace characters |
| manage_ancillary | string | `free standing` | Management practices relating to the ancillary use code(s)
| land_estate | string | `freehold` | Estate type |
| land_status | string | [TBD] | Land status type (public–private continuum; terminology to be determined) |
| water | string | `lake` | Water type (`null` for non-water) |
| zone | string | `Large format retail zone` | District plan zone; terminology to be taken from the Zone Framework Standard (National Planning Standards, 2019) |
| permeability | string | `sealed` | Permeability type (`sealed` or `unsealed`) |
| confidence | integer | `3` | Confidence 1-4, a qualitative assessment relating to the overall operator confidence in the assigned classification |
| luc_date | date | `2024-05-26` | Date of land use classification, "last modified" |
| comment | string | `Pūkaha National Wildlife Centre | Optional, arbitrary comment that may provide additional contextual information, name/s, note/s, etc. For classifications rlelated to legal protection, the relevant information (e.g. the Act) should be recorded within this field, but it may not be the only content. UTF-8 character encoding. |
| source_data | (sorted set of) string | `DVR,NRC,LCDB v5,field mapping` | Primary source data (e.g. field mapping, local knowledge, ancillary dataset, air photo, imagery). Often, multiple sources of information are combined to come to a conclusion; to a reasonable extent, all should be specified. |
| source_data_doi | (set of) uri | `doi:10.26060/W5B4-WK93` | Optional (i.e. when available) DOI or HTTP URI for source data |
| source_date | string (date range) | `[2011-05-02,2025-01-03)` | Combined date range of spatial features (e.g. image date, ancillary photo date, last edited date) in primary source data, at feature (preferentially) or dataset level, using interval notation for inclusive and exclusive endpoints |
| source_scale | string (integer interval) | `[10,60]` | Combined integer (interval)[https://en.wikipedia.org/wiki/Interval_(mathematics)] indicating the precision of source data, in the CRS units (metres) |

## Commodities

Accepted commodities are similar to those accepted for [use in ALUM v8, Table 2](https://www.agriculture.gov.au/abares/aclump/land-use/alum-classification). The term list is available as:

- [Markdown table](build/commodities.md)
- [Excel spreadsheet](build/commodities.xlsx)
- [RDF (Turtle)](rdf/term-lists/commodities.ttl)

## Management practices

Accepted management practices are those accepted for [use in ALUM v8, Table 3](https://www.agriculture.gov.au/abares/aclump/land-use/alum-classification) The term list is available as:

- [Markdown table](build/management-practices.md)
- [Excel spreadsheet](build/management-practices.xlsx)
- [RDF (Turtle)](rdf/term-lists/management-practices.ttl)

## Tenure

Information relating to land tenure should be captured in two attributes: `land_estate` and `land_status`. How land is owned, and by whom, is an important consideration for how land may be used or managed. This information is included because it directly participates in the intended use of the land use classification system, though it is auxiliary.

Please see: [LINZ: Tenure review](https://www.linz.govt.nz/our-work/crown-property-management/pastoral-land/tenure-review)

### `land_estate`

Controlled vocabulary of types of tenure in New Zealand

- `freehold` or (to be more specific) `māori freehold`, i.e. estate in fee simple
- `leasehold` or (to be more specific) `crown leasehold` (e.g. a Crown pastoral lease)
- `cross lease`
- `stratum estate`, i.e. forms of unit title, according to whether land that has been subdivided was freehold or leasehold; `stratum estate in freehold`, `stratum estate in leasehold` (to be more specific)

### `land_status`

A non-exhaustive list of land status types organised along a gradient from Crown (public) to private.

_To be determined_: a controlled vocabulary to describe these by reference to some systematic grouping and authoritative list of terms.

1. Crown
    1. Department of Conservation
    1. Territorial Local Authorities
        1. Regional councils
        1. Unitary authorities
        1. City councils
        1. District councils
    1. Offices of Parliament
    1. State services departments
        1. Public service departments
        1. Departmental agencies
        1. State services organisations outside the core public service, e.g.
            - NZDF
            - NZ Police
    1. Land Information New Zealand (LINZ), with respect to unallocated Crown land
1. Intermediate
    1. State-owned enterprises, e.g.
        - AsureQuality
        - Electricity Corporation of New Zealand
        - Kiwirail
        - Landcorp
        - MetService
        - Transpower New Zealand
    1. State-(part-)owned enterprises, e.g.
        - AgResearch
        - Air New Zealand (51.95% government ownership)
        - Christchurch Airport (25%)
        - Housing New Zealand Corporation
        - Landcare Research
        - Genesis Energy Limited (52.4%)
        - Mercury Energy (51.15%)
        - Meridian Energy (51.02%)
        - Scion
        - Plant & Food Research
    1. Non-SOE Crown-owned companies, e.g.
        - Crown Research Institutes
        - TVNZ
        - RNZ
    1. Universities
    1. Institutes of Technology and Polytechnics
    1. Wānanga (those that have been granted _Crown entity_ status)
    1. Council-controlled organisations (e.g. Ports of Auckland)
1. Private
    1. Businesses (corporations, companies)
    1. Trusts
    1. Families
    1. Individuals
    1. Iwi


## Geographic scale

The intended geographic unit of this classification system is the property parcel. However it may be appropriate to map sub-parcel geographic entities for particular classes, particularly if the boundary of natural features (forests, waterways) is pertinent, if the parcel is very large, and where source data scale permits such definition. Whether to map sub-parcel areas is therefore left to operator discretion, but the intended and minimum level of attribution is the property parcel, and therefore property parcel identifiers and geographic boundaries must be present in output land use data.

## `source_scale`

To indicate that one of the endpoints is to be excluded from the set, use a parenthesis and not a square bracket (the latter indicates inclusion). For example, if source data is precise between 0.02 and 0.75 metres, use the notation `(0,1)`, indicating precision at the sub-metre scale, between 0-1 m (but not including the endpoints). If vector data is no more precise than 60 m, use `[60,)` if there is no suitable upper-bound; or else determine an appropriate nominal upper-bound since (i.e. `[60,x]`, where x > 60) as it is unlikely that in reality there is no upper bound.

Rules of thumb for converting nominal scales of input data to this notation:

- Raster data pixel size: given the smaller of the pixel height or width (a) and the larger of the height or width (b): `[a,b]`. If a = b, this notation is still appropriate as `[a,a]` would be the singleton set `{a}`, whereas `(a,a)` is not correct notation as it is an empty set. Example: a raster with 30 metre pixels: `[30,30]`.
- `1:50000` scale map data, as in LINZ topographic data for the 1:50,000 map series (no further information available about how data is produced): precision = (map scale denominator) / 1,000. For example, a 1:50,000 scale map has a positional precision of about 50 metres. Denote this as `[50,)`, (with an optional practical or QA-derived upper limit).
- A map produced from raster data with 10 metre pixels, manually digitised at 1:25,000 scale. In this case the errors are explicit and cumulative. Precision = 10 + 25,000/1,000 = 35. Therefore record as `[35,)` (with an optional practical or QA-derived upper limit).

If multiple input datasets are used together to come to a classification decision, the ranges should be merged. That is, compute the smallest range that includes all of the given ranges. (See the `range_merge` function in PostgreSQL). For example, the ranges `[1,2)` and `[3,4)` can be combined to form `[1,4)`.

## Temporality

Interannual. A crop planted for a whole year is a commodity, but not necessarily a land use e.g. if it's part of livestock farm system. The primary economic purpose over an interannual period is the determining factor for the assignment of a land-use class. 

## Data format and spatial referencing

Vector data format: [GeoPackage](https://www.geopackage.org/) v1.4.0 or later and/or [GeoParquet](https://geoparquet.org/) v1.0.0 or later.

Raster data (or other formats) _may_ be produced for user convenience, but no particular format is specified, due to the lack of wide acceptance of a raster data format with support for attribute tables. Vector data is mandatory, however.

Coordinate system: any [current official projection](https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/projections) may be used:

- New Zealand Transverse Mercator 2000 (NZTM2000).
- NZGD meridional circuits (e.g. for regional extracts) or offshore island projections.
- New Zealand Continental Shelf Lambert Conformal 2000 (NZCS2000).


## Suggested colour scheme (at the secondary scale)

| Colour | Class Code | Category | Hex Code |
|:--:|:--:|---|---|
| ![7F6DF2](https://place-hold.it/50x50/7F6DF2/7F6DF2.png&text=7F6DF2) | 1.1.0 | **Biodiversity protection** | `#7F6DF2` |
| ![A88BE0](https://place-hold.it/50x50/A88BE0/A88BE0.png&text=A88BE0) | 1.2.0 | **Cultural and natural heritage** | `#A88BE0` |
| ![CAB4D4](https://place-hold.it/50x50/CAB4D4/CAB4D4.png&text=CAB4D4) | 1.3.0 | **Minimal use from relatively natural environments** | `#CAB4D4` |
| ![D6C8DA](https://place-hold.it/50x50/D6C8DA/D6C8DA.png&text=D6C8DA) | 1.4.0 | **Unused and transitioning land** | `#D6C8DA` |
| ![37966F](https://place-hold.it/50x50/37966F/37966F.png&text=37966F) | 2.1.0 | **Plantation forests** | `#37966F` |
| ![A5D64B](https://place-hold.it/50x50/A5D64B/A5D64B.png&text=A5D64B) | 2.2.0 | **Grazing modified pasture systems** | `#A5D64B` |
| ![E7F281](https://place-hold.it/50x50/E7F281/E7F281.png&text=E7F281) | 2.3.0 | **Short-rotation and seasonal cropping** | `#E7F281` |
| ![F8DB76](https://place-hold.it/50x50/F8DB76/F8DB76.png&text=F8DB76) | 2.4.0 | **Perennial horticulture** | `#F8DB76` |
| ![EEC22D](https://place-hold.it/50x50/EEC22D/EEC22D.png&text=EEC22D) | 2.5.0 | **Intensive horticulture** | `#EEC22D` |
| ![A66E4A](https://place-hold.it/50x50/A66E4A/A66E4A.png&text=A66E4A) | 2.6.0 | **Intensive animal production** | `#A66E4A` |
| ![4DA6FF](https://place-hold.it/50x50/4DA6FF/4DA6FF.png&text=4DA6FF) | 2.7.0 | **Water and wastewater** | `#4DA6FF` |
| ![BFD3C1](https://place-hold.it/50x50/BFD3C1/BFD3C1.png&text=BFD3C1) | 2.8.0 | **Vacant and transitioning land** | `#BFD3C1` |
| ![FFBEBE](https://place-hold.it/50x50/FFBEBE/FFBEBE.png&text=FFBEBE) | 3.1.0 | **Residential** | `#FFBEBE` |
| ![FF5500](https://place-hold.it/50x50/FF5500/FF5500.png&text=FF5500) | 3.2.0 | **Public recreation and services** | `#FF5500` |
| ![FF0000](https://place-hold.it/50x50/FF0000/FF0000.png&text=FF0000) | 3.3.0 | **Commercial** | `#FF0000` |
| ![8C2F39](https://place-hold.it/50x50/8C2F39/8C2F39.png&text=8C2F39) | 3.4.0 | **Manufacturing and industrial** | `#8C2F39` |
| ![D16B7F](https://place-hold.it/50x50/D16B7F/D16B7F.png&text=D16B7F) | 3.5.0 | **Utilities** | `#D16B7F` |
| ![A80084](https://place-hold.it/50x50/A80084/A80084.png&text=A80084) | 3.6.0 | **Transport and communication** | `#A80084` |
| ![5A5C6C](https://place-hold.it/50x50/5A5C6C/5A5C6C.png&text=5A5C6C) | 3.7.0 | **Mining** | `#5A5C6C` |
| ![4A5568](https://place-hold.it/50x50/4A5568/4A5568.png&text=4A5568) | 3.8.0 | **Waste treatment and disposal** | `#4A5568` |
| ![E5E5E5](https://place-hold.it/50x50/E5E5E5/E5E5E5.png&text=E5E5E5) | 3.9.0 | **Vacant and transitioning land** | `#E5E5E5` |



## References

[^1]: Cavanagh J, Whitehead B 2022. Land-use classification for state of the environment soil quality monitoring and reporting. Manaaki Whenua – Landcare Research contract report LC4146. https://www.envirolink.govt.nz/assets/Envirolink/2222-GSDC170- Land-use-classification-for-state-of-the-environment-soil-quality-monitoring-and- reporting.pdf

[^2]: Cavanagh J, Whitehead B 2023. Enabling flexibility and connectivity in land-use classification for state of the environment soil quality monitoring. Manaaki Whenua – Landcare Research contract report LC4309 for Land Monitoring Forum. https://www.envirolink.govt.nz/assets/Envirolink/R18-4-Enabling-flexibility-and- connectivity-in-land-use-classification-for-state-of-the-environment-soil-quality- monitoring.pdf

[^3]: Rutledge D, Cameron M, Briggs C, Elliott S, Fenton T, Hurkens J, et al. 2016. WISE: Waikato Integrated Scenario Explorer. Technical Report #3506882. Waikato Regional Council

[^4]: Price R, Rutledge D, Fraser M 2010. New Zealand Land Use Database. Envirolink Project LCRX0901 Draft Database Design Report

[^5]: MfE (Ministry for the Environment) 2019. National planning standards. https://environment.govt.nz/publications/national-planning-standards/

[^6]: LINZ (Land Information New Zealand) 2010. Rating valuations rules 2008: version date 1 October 2010 – LINZS30300. https://www.linz.govt.nz/resources/regulatory/rating- valuations-rules-2008-version-date-1-october-2010-linzs30300

[^7]: Bellingham PJ, Overton JMcC, Thomson FJ, MacLeod CJ, Holdaway RJ, Wiser SK, Brown M, Gormley AM, Collins D, Latham DM, Bishop C, Rutledge DT, Innes JG, Warburton B 2016 Standardised terrestrial biodiversity indicators for use by regional councils. Landcare Research Contract Report LC2109 prepared for Regional Councils' Biodiversity Monitoring Working Group, Auckland Council, Auckland, New Zealand.

[^8]: Planzer S, Bellis S, Gatiso T 2024. Protected Areas Network New Zealand methodology review and report. Phase II – stakeholder engagement. Manaaki Whenua – Landcare Research contract report LC4446. 
