# New Zealand Land Use Management and Tenure (NZLUMT) Classification System 

Status: Draft
Version: 0.1
Developed by: Manaaki Whenua – Landcare Research

> Kotahi te aho ka whati, ki te kāpuia e kore e whati.
>
> One strand of flax is easy to break, but many strands together will stand strong.
> 
> — Kīngi Tāwhiao

<!-- ## TODO

- [ ] Temporality
- [ ] 1.1 and 1.2 model according to Bellingham 2016 and IUCN, as an equivalent to ALUM's CAPAD
- [ ] Hunting, open and restricted https://www.doc.govt.nz/map/index.html (management practice on conservation land?) e.g. `hunting`, `hunting open`, `hunting restricted`, `hunting prohibited` (restricted doesn't mean prohibited).
- [ ] Permanent forests under the ETS, https://www.mpi.govt.nz/forestry/funding-tree-planting-research/closed-funding-programmes/permanent-forest-sink-initiative/  3.1.4. Environmental Forest Plantation
- [ ] Carefuly review class definitions for application to New Zealand
- [ ] Add a note on tenure review process for crown leasehold land in the South Island

-->

## Overview

NZLUMT is an adaptation of the Australian Land Use and Management (ALUM) Classification (version 8) for application in New Zealand. Where direct overlap is considered appropriate, it is retained. If there is some degree of incompleteness in the specification, ALUM practice and guidance can be assumed to be applicable. ALUM is licensed under a [Creative Commons Attribution 3.0 Australia Licence](https://creativecommons.org/licenses/by/3.0/au), which explicitly permits adaptation of ALUM.

The NZLUMT is intended for the purpose of land use change modelling and environmental monitoring (especially for fresh water management). Land use practices are of particular relevance to this classification system, as there is a need to understand social and economic capacity for changes to land management practices. Land tenure is also a compulsory attribute as it relates to the potential for changes to land use and land use management practices (i.e. tenure may constrain possibile changes).

<!-- TODO explicitly form some enduring questions that can be answered using this classification system -->

It balances simplicity of use with with flexibility and extensibility.

> Stiving to better, oft we mar what's well

— Duke of Albany, _King Lear_ (Shakespeare, 1606)

In other terms, the perfect is the enemy of the good. Implementations of this classification system should accept and record available yet partial information. For example, where it is clear that there is a plantation forest, but the intended _use_ of the timber (i.e. a commodity such as `pulp` or `sawlogs`) is _not_ apparent, the land use should still be attributed to an appropriate plantation forestry class, but the commodity value left as a null value. Record what is known, even where there are known information gaps.

Describing _how_ a classification is known is an important classification framework principle ("Priorite reproducible and transparent methodologies").

1. Through the recording of loose provenance information as part of the data schema (`source_data`, `source_data_doi`, `source_date`, and `source_scale`). This is not especially rigorous and is intended for rapid end-user information.
<!-- TODO 2. As a more rigourous but optional addition, describing classification logic using semantic techniques -->

## Hierarchical Classification System

![NZLUMT hierarchical classification system as a table](./NZLUMT.svg)

1. **Conservation and natural environments**

    This class includes land that has a relatively low level of human intervention. The land may be formally reserved by government for conservation purposes, or conserved through other legal or administrative arrangements. Areas may have multiple uses, but nature conservation is a central consideration. Some land may be unused as a result of a deliberate decision of government or landowner, or due to circumstance.

    Where a classification is made on the basis of information about legal protection, the relevant information (e.g. the Act) should be mentioned in the `comment` field.

    <details><summary>Expand</summary>

    1. **Nature conservation**

        Tertiary classes 1.1.1–1.1.3 are based on the classification for areas legally protected for biodiversity, as proposedby Bellingham (2016, Tables 15-6, 15-7) <!-- TODO file:///home/lawr/Downloads/bellingham-etal_2016_standardised-terrestrial-biodiversity-indicators-for-use-by-regional-councils.pdf Table 15-7 -->

        1. **High degree of biodiversity protection** (Bellingham Rank 5); protection is the main purpose or is ranked equally with a limited number of other compatible purposes. Examples:
        - National Parks Act 1980
            - National Park
        - Reserves Act 1977
            - Nature Reserve
            - Scientific Reserve
        - Conservation Act 1987
            - Sanctuary Area
            - Wilderness Area
            - Wildlife Management Area
        - Resource Management Act 1991
            - Water Conservation Order
        - Wildlife Act 1953
            - Wildlife Sanctuary
        1. **Moderately high degree of biodiversity protection** (Bellingham Rank 4); protection is a main purpose but is shared with other, less compatible purposes (i.e. recreation). Examples:
        - Conservation Act 1987
            - Amenity Areas
            - § 23 Watercourse Area
        - Reserves Act 1977
            - Conservation Covenant
            - Protected Private Land
            - Scenic Reserve
        - Conservation Act 1987
            - Conservation Park
            - Ecological Area
        - Te Ture Whenua Māori Act 1993
            - Māori Reservation (Wetland or Scenic Reserve)
        - Queen Elizabeth II National Trust Act 1977
            - QEII Open Space Covenant
        - Wildlife Act 1953
            - Wildlife Refuge
        1. **Moderate degree of biodiversity protection** (Bellingham Rank 3); protection is a desired purpose but subject to capability with a different main purpose or may be less comprehensive (i.e. only some aspects of biodiversity protection are targeted). Examples:
        - Conservation Act 1987
            - Ecological Area
            - Stewardship Area
        - Reserves Act 1977
            - Government Purpose Reserve (Ecological or Wildlife)
            - Ngā Whenua Rāhui Kawenata
            - Local Purpose Reserve (Ecological)
        - Te Ture Whenua Māori Act 1993
            - Māori Reservation (Conservation or Conservation of Native Bush)
        - Wilidlife Act 1953
            - Wildlife Management Reserve

    2. **Managed resource protection**

        Tertiary classes 1.2.1–1.2.2 are based on the classification for areas legally protected for biodiversity, as proposedby Bellingham (2016).

        1. **Moderately low degree of biodiversity protection** (Bellingham Rank 2); some biodiversity protection is achieved but it of secondary importance. Examples:
        - Resource Management Act 1991
            - Esplanade Reserve or Strip
            - Consent Notice (i.e. subdivisions granted subject to conditions to be complied with on a continuing basis by the subdividing land owner and subsequent owners)
        - Reserves Act 1977
            - Historic Reserve
            - Local Purpose Reserve (Other – various)
            - Recreation Reserve
        - Te Ture Whenua Māori Act 1993
            - Māori Reservation (various purposes related to Recreation, Camping, Water Supply, Meeting Places, Historic Significance, etc.)
        - Conservation Act 1987
            - Marginal Strip
        - Local Government Act 2002
            - Regional Parks

        1. **Low degree of biodiversity protection** (Bellingham Rank 1); protection results indirectly and fortuitously as a result of other actvities. Examples:
        - Te Ture Whenua Māori Act 1993
            - Māori Reservation (various purposes related to Marae, Pā Sites, Papakāinga, Urupā, Wāhi Tapu, etc.)
        - River Boards Act 1908
            - River Bed
        - Reserves Act 1977
            - Road Reserve

    3. **Sustainable use from relatively natural environments**

        This class includes land that is subject to relatively low levels of intervention. The land may not be used more intensively because of its limited capability. The structure of the native vegetation generally remains intact despite deliberate use, although the floristics of the vegetation may have changed markedly. Where the native vegetation structure is, for example, open woodland or grassland, the land may be grazed.

        Where native grasses have been deliberately and extensively replaced with other species, the use should be treated under class 3.

        1. **Production native forests**

        Commercial production from non-plantation native forests and related activities on public and private land. Environmental and indirect production uses associated with retained native forest (e.g. prevention of land degradation, windbreaks, shade and shelter) are included in classes 1.1 or 1.2.

        This class includes wood production forestry on native timber without clearfelling, and other native forest production (non-sawlog or non-pulpwood production, including oil, wildflowers, firewood, fence posts, and mānuka/kānuka honey).

        1. **Mahinga kai**

        Food gathering practices from natural environments. This is often an ancillary use; this class should only be assigned to the `lu_code` if the collection of food is indeed the prime use of land (but it may often be listed as an ancillary use). If food gathering is done commercially, _and_ if the environment is considerably altered as a result of the practice, it should be classified under class 2.

        <!-- TODO discuss "foraging" of natural environments as a potential use, e.g. seafood gathering, manuka honey, truffle, possibly hunting -->

    4. **Other minimal use**

        Areas of land that are largely unused (in the context of prime use) but may have ancillary uses. This may be a deliberate decision by the land manager or the result of other circumstances. The land may be available for use but remain unused for various reasons.

        1. **Defence land** Natural areas allocated to field training, weapons testing and other field defence uses, predominantly in rural areas.

        2. **Residual native cover** Land under native cover, mainly unused (no prime use) or used for non-production or environmental purposes (e.g. to conserve native vegetation and wildlife, or for natural resources protection). This class is only appropriate where there is no applicable prime use or where land use is indeterminate. For example livestock may occasionally graze, but where grazing is the intended prime use of the land, it should be classed under 2.1.0 or 3.2.1. Corridors and roadside areas may fit under this class, along with unusable land such as cliffs, rock faces, boulders and tors, provided there are relatively low levels of disturbance. Where there has been significant disturbance to the land (e.g. clearing) the area should be assigned to a non-conservation land use.

        3. **Rehabilitation** Land under rehabilitation that has been restored to a near natural state. Land that is degraded or undergoing rehabilitation but still substantially modified should be mapped under 3.6.2, 3.6.3, 4.6.2, 4.6.3 or 5.8.4.

    </details>

2. **Production from agriculture and plantations**

    This class includes land that is used principally for primary production. Native vegetation has largely been replaced by introduced species through clearing, the sowing of new species, the application of fertilisers or the dominance of volunteer species. The range of activities in this category includes plantation forests, pasture production for stock, cropping and fodder production, and a wide range of horticultural production. If there is evidence of irrigation infrastructure, land should have irrigation listed as a management practice even if irrigation water has not been applied in the current growing season.

    Fallow or ploughed land should be assigned to the most likely land use based on the dominant activity conducted in comparable nearby areas. Fallow or ploughed land should be allocated to the relevant pasture, cropping or horticulture class (rather than using land in transition). Record the fallow or ploughed status in the management field.
   
    <details><summary>Expand</summary>

    1. **Plantation forests**

        Land on which plantations of trees or shrubs (native or exotic species) have been established for production, or environmental and resource protection purposes. This includes farm forestry. Where planted trees are grown in conjunction with pasture, fodder or crop production, class allocation should be made on the basis of prime use.

        1. **Hardwood plantation forestry**
        2. **Softwood plantation forestry**
        3. **Other forest plantation**
        4. **Environmental forest plantation**

    2. **Grazing modified pastures**

        <!-- TODO Management practices: dairy wintering on/off, dairy support blocks -->
        
        Pasture and forage production, both annual and perennial, based on significant active modification or replacement of the initial vegetation.

        Land under pasture at the time of mapping may be in a rotation system, so that at another time the same area may be, for example, under cropping. Land in a rotation system should be classified according to the prime use (if known) or the land use at the time of mapping, with rotation information recorded in the management field. If the rotation sequence is known record this in the comments field. Effort should be made to distinguish a land use change from a rotation.

        If livestock or pasture type is known, record this in the commodity field.

        Some management practices relate to particular commodities. For example, `dairy cattle` (commodity) can be included alongside (`wintering off`) to describe a dairy farm system which practices wintering off. These practices should be recorded if known. Other relevant management practices in this case are:

        - `wintering off`
        - `feed pad`
        - `stand-off pad`
        - `herd home`
        - `composting barn`
        - `sacrifice paddock`

        1. **Native/exotic pasture mosaic**
        2. **Wood fooder plants**
        3. **Pasture legumes**
        4. **Pastre legume/grass mixtures**
        5. **Sown grasses**

    3. **Cropping**

        Land that is under cropping. Land under cropping at the time of mapping may be in a rotation system, so that at another time the same area may be, for example, under pasture. Land in a rotation system should be classified according to the prime use (if known) or the land use at the time of mapping, with rotation information recorded as a management practice. If the rotation sequence is known record this as a comment.

        Cropping can vary markedly over relatively short distances in response to changes in the nature of the land and the preferences of the land manager. It may also change over time in response to market conditions. Production of fodder, such as lucerne hay, is considered cropping as there is no harvesting by stock. Strip cropping—where multiple commodities are cropped simultaneously—can be assigned to the secondary class 3.3 with multiple commodities recorded using the commodity field, and cropping strip in the management field.

        If the type of crop type is known, record this in the commodity field using the commodity list.

        1. **Cereals**
        1. **Beverage and spice crops**
        1. **Hay and silage**
        1. **Oilseeds**
        1. **Pulses**

    4. **Perennial horticulture**

        Crop plants living for _more than two years_ that are intensively cultivated, usually involving a relatively high degree of nutrient, weed and moisture control. If the crop type is known use the commodity list to record this. Management practices such as irrigation, or netting to protect crops from hail or birds can be recorded as management practices.

        1. **Tree fruits**
        2. **Tree nuts**
        3. **Vine fruits**
        4. **Shrub berries and fruits**
        5. **Perennial flowers and bulbs**
        6. **Perennial vegetables and herbs**

    5. **Seasonal horticulture**

        Crop plants living for _less than two years_ that are intensively cultivated, usually involving a relatively high degree of nutrient, weed and moisture control. If the crop type is known the commodity list should be used to record this. If irrigation infrastructure is present, record it as a management practice.

        1. Seasonal fruits
        2. Seasonal flowers and bulbs
        3. Seasonal vegetables and herbs
        4. Turf farming

    6. **Land in transition**

        Areas where the land use is unknown and cannot reasonably be inferred from the surrounding land use. This class should be used sparingly. If possible, fallow or ploughed land should be allocated to a relevant pasture, cropping or horticulture class as this is the primary use. Land must previously have been used for agriculture or plantations.

        1. Degraded land
        2. Abandoned land

    </details>

3. **Intensive Uses**

    This class includes land uses that involve high levels of interference with natural processes, generally in association with closer settlement. The level of intervention may be high enough to completely remodel the natural landscape—the vegetation, surface and groundwater systems, and the land surface. If crop and/or animal type is known, record this in the commodity field.

    <details><summary>Expand</summary>

    1. **Intensive horticulture**
        
        Intensive forms of plant production often with special purpose improvements used for horticultural production. If crop type is known, record this in the commodity field.

        1. **Production nurseries**
        2. **Shadehouses**
        3. **Glasshouses**
        4. **Glasshouses—hydroponic**
        5. **Abandoned intensive horticulture**

    2. **Intensive animal production**

        Intensive forms of animal production (excludes associated grazing or pastures), livestock production facilities or animal-holding yards. If the animal type is known, record this in the commodity field. The management field can be used to record practices such as free range or milking system.

        1. **Dairy sheds and yards**
        2. **Feedlots**
        3. **Poultry farms**
        4. **Piggeries**
        5. **Aquaculture**
        6. **Horse studs**
        7. **Saleyards/stockyards**
        8. **Abandoned intensive animal production**

    3. **Manufacturing and industrial**

        Factories, workshops, foundries, construction sites and so on. In the urban setting, manufacturing and industrial areas should be mapped to this secondary code. In the rural or agricultural setting, the following tertiary classes may be used if desired.

        1. **General purpose factory**
        2. **Food processing factory**
        3. **Major industrial complex**
        4. **Bulk grain storage**
        5. **Abattoirs**
        6. **Oil refinery**
        7. **Sawmill**
        8. **Abandoned manufactuing and industrial**

    4. **Residential and farm infrastructure**

        Land with houses and or other residential infrastructure with or without associated agricultural activity. This class includes urban and remote communities, farm buildings and other farm infrastructure larger than the minimum mapping scale, and land in transition to residential from other land uses. This class also includes holiday shacks.

        1. **Urban residential**
        2. **Lifestyle without agriculture**
        3. **Lifestyle with agriculture**
        4. **Farm buildings/infrastructure**
    
    5. **Services**

        Land allocated to providing commercial or public services, resulting in substantial interference to the natural environment. Where services are provided on land that retains natural cover, apply an appropriate classification under class 1.

        1. **Commercial services**
        2. **Public services**
        3. **Recreation and culture**
        4. **Defence facilities—urban**
        5. **Research facilities**
    
    6. **Utilities**

        Land allocated to providing electricity, gas, or water.

        1. **Fuel powered electricity generation**
        2. **Hydro electricity generation**
        3. **Wind electricity generation**
        4. **Solar electricity generation**
        5. **Electricity substations and transmission**
        6. **Gas treatment, storage and transmission**
        7. **Water extraction and transmission**

    7. **Transport and communication**

        Land allocated to infrastructure used for transportation of goods or people, or navigation and communication equipment.

        1. **Airports/aerodromes**
        2. **Roads**
        3. **Railways**
        4. **Ports and water transport**
        5. **Navigation and communication**

    8. **Mining**

        Mining and extractive industries (excluding salt extraction from evaporation basins). Record the type of mining if known, from the commodity field.

        1. **Mines**
        2. **Quarries**
        3. **Tailings**
        4. **Extractive industry not in use**

    9. **Waste treatment and disposal**

        Waste material and disposal facilities associated with industrial, urban and agricultural activities.

        1. **Effluent pond**
        2. **Landfill**
        3. **Solid garbge**
        4. **Incinerators**
        5. **Sewage/sewerage**

    </details>

## Tenure

Information relating to land tenure should be captured in two attributes: `land_estate` and `land_status`. How land is owned, and by whom, is an important consideration for how land may be used or managed. This information is included because it directly participates in the intended use of the land use classification system, though it is auxiliary.

### `land_estate`

Controlled vocabulary of types of tenure in New Zealand

- `freehold` or (to be more specific) `māori freehold`, i.e. estate in fee simple
- `leasehold` or (to be more specific) `crown leasehold` (e.g. a Crown pastoral lease)
- `cross lease`
- `stratum estate`, i.e. forms of unit title, according to whether land that has been subdivided was freehold or leasehold; `stratum estate in freehold`, `stratum estate in leasehold` (to be more specific)

### `land_status`

A non-exhaustive list of land status types organised along a gradient from Crown (public) to private.

<!-- TODO controlled vocabulary to describe these by reference to some systematic grouping -->

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

## Water

Water is a land cover, rather than a land use. (If it is considered "land" at all.) Certain land uses can only occur on water (e.g. aquaculture); some can occur on either land or water (e.g. oil and gas wells); some only on land (e.g. pastoral farming)—but pieces of such land may include water, e.g. dams, ponds, and lakes.

ALUM classifies water as a primary class, but notes that this presents some difficulty. NZLUMT specifies instead that water is to be recorded as a distinct attribute that can be applied to a geographic unit.

Very often water doesn't occupy the entire geographic unit (i.e. parcel); it should still be discriminated accurately as a sub-parcel-scale feature. The exception is if it is very small, in which case it can be ignored rather than attributed to the entire parcel.

The "water" field can take one of the following values:
    - `lake`
    - `reservoir`
    - `dam`
    - `evaporation basin`
    - `river`
    - `channel`
    - `aqueduct`
    - `wetland`
    - `estuary`
    - `intertidal` <!-- supralittoral, eulittoral -->
    - `marine` <!-- sublittoral -->

## General issues

### Geographic scale

The intended geographic unit of this classification system is the property parcel. However it may be appropriate to map sub-parcel geographic entities for particular classes, particularly if the boundary of natural features (forests, waterways) is pertinent, if the parcel is very large, and where source data scale permits such definition. Whether to map sub-parcel areas is therefore left to operator discretion, but the intended and minimum level of attribution is the property parcel, and therefore property parcel identifiers and geogaphic boundaries must be present in output land use data.

### Temporality

<!-- Interannual. A crop planted for a whole year is a commodity, but not neccessarily a land use e.g. if it's part of livestock farm system... primary economic purpose is the determining factor for landuse class -->

## Data specifications

### Data structure

<!-- TODO make example realistic, e.g. coherent class examples -->
| attribute | type | example | notes |
| --- | --- | --- | --- |
| lu_coden | integer | `123` | Numerical land use code (primary use)|
| lu_code | string | `1.2.3` | Land use code (primary use) |
| lu_description | string | `Groundwater` | Land use class label (primary use) |
| lu_code_ancillary | string | `2.2.0, 3.2.1` | Land use code (ancillary uses), multiple uses are to be specified with comma separation with optional whitespace characters |
| commod | string | `cattle dairy` | Commodity type; multiple commodities are to be specified with comma separation with optional whitespace characters |
| commod_ancillary | string | `pulpwood` | Commodity type(s) relating to the ancillary land use code(s) |
| manage | string | `irrigation spray, organic` | Management practices; multiple practices are to be specified with comma separation with optional whitespace characters |
| manage_ancillary | string | `free standing` | Management practices relating to the ancillary use code(s)
| land_estate | string | `freehold` | Estate type |
| land_status | string | TBD | Land status type (public-private continuum) |
| water | string | `lake` | Water type (null for land) |
| confidence | integer | `3` | Confidence 1-4, a qualitative assessment relating to the overall operator confidence in the assigned classification |
| luc_date | date | `2024-05-26` | Date of (primary) land use code |
| source_data | string | `Northland Regional Council` | Primary source data (e.g. field mapping, local knowledge, ancillary dataset, air photo, imagery). Often, multiple sources of information are combined to come to a conclusion; only ony should be specified. |
| source_data_doi | uri | `doi:10.26060/W5B4-WK93` | Optional (i.e. when available) DOI or HTTP URI for the source data |
| source_date | date | `2023-12-01` | Date of spatial featue (e.g. image date, ancillary photo date) in primary source data |
| source_scale | string | `1:25000` | Scale of primary source data

### Data format and spatial referencing

Vector data format: [GeoPackage](https://www.geopackage.org/) v1.4.0 or later and/or [GeoParquet](https://geoparquet.org/) v1.0.0 or later.

Raster data (or other formats) _may_ be produced for user convenience, but no particular format is specified, due to the lack of wide acceptance of a raster data format with support for attribute tables. Vector data is mandatory, however.

Coordinate system: any [current official projection](https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/projections) may be used:

- New Zealand Transverse Mercator 2000 (NZTM2000).
- NZGD meridional circuits (e.g. for regional extracts) or offshore island projections.
- New Zealand Continental Shelf Lambert Conformal 2000 (NZCS2000).

# References

Bellingham PJ, Overton JMcC, Thomson FJ, MacLeod CJ, Holdaway RJ, Wiser SK, Brown M, Gormley AM, Collins D, Latham DM, Bishop C, Rutledge DT, Innes JG, Warburton B 2016 Standardised terrestrial biodiversity indicators for use by regional councils. Landcare Research Contract Report LC2109 prepared for Regional Councils' Biodiversity Monitoring Working Group, Auckland Council, Auckland, New Zealand.