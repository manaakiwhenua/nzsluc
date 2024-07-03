## Glossary

- **Discrete Global Grid Systems (DGGS)**: multi-resolution grids defined on the surface of regular polyhedra (such as the icosahedron) and projected onto a sphere to create multi-resolution geospatial data structures that are global in extent without singularities (Sahr et al. 2003)[^1]. A DGGS can be used as a hybrid raster-vector geospatial data model and has recently been employed in land-use classification (Law & Ardo 2023)[^2], but its application is not limited to land use. 
<!-- Sahr -->
<!-- TODO Law & Ardo 2023 citation -->

- **Geographical unit**: the geographical entity or entities to which a land-use classification (or relevant attributes) is associated. Many land-use classification systems attempt to classify parcels of land; the parcel is therefore the geographical unit. The appropriate unit may range from plot, field, farm or catchment to region; the concept is therefore one of geographical scale. The geographical unit may not be a specific type of geographical object a person may recognise; it may be a small, arbitrary raster or discrete global grid cell, or areas that appear sufficiently homogeneous from a remote-sensing perspective to be treated as a group, but which may have no legal association.

- ***Land-use capability**: primarily an evaluation of productive capacity depending on the physical qualities of the land, soil, and environment. Key factors assessed are susceptibility to erosion, steepness of slope, climate, susceptibility to flooding, liability to wetness or drought, salinity, and the depth, texture, structure, and nutrient supply of the soil (Lynn et al. 2009)[^3].
<!-- TODO Lynn et al citation -->

- **Land-use classification framework**: a wider system of guidelines and governance around a land-use classification system; for example:  
    - the framework of review that is applied to the Australian Land Use and Management (ALUM) classification system 
    - the guidelines for how ALUM itself is structured (e.g. that it should be hierarchical, general-purpose, and may record ancillary uses as well as a primary use)
    - the decision to align the classification with the Australian Spatial Data Infrastructure (ASDI) standard for land-use data sets, and to publish an environmental vocabulary service to make the classification system machine interpretable.  

    The framework may determine how to record information that is ancillary to the land-use information itself (i.e. a data schema that goes beyond a vocabulary). This may include provenance information, commodities, management practices, and how to present confidence and geographical scale to end-users of the land-use data product. 

- **Land-use classification system**: narrower than a land-use classification framework and sits within one. It is the system of labels or terms used to describe land use, and structure (categorial, hierarchical), and often a system of numerical encoding. 

- **Land-use information system**: a collection of software and tools designed for the specific task of classifying land use. This often requires the integration of substantial amounts of geospatial data and the development of complex classification rules.2 

- **Land-use intensity**: the amount of a thing per unit area, which may refer to attributes such as stocking rates, fertiliser application, or population density. 

- **Land-use suitability**: broadly speaking, the ‘fitness’ of a given piece of land for a defined land use. The process of land suitability classification involves the appraisal and grouping of specific areas of land in terms of their absolute or relative suitability for a defined use, as determined by a specific set of diagnostic criteria. In this regard land-use capability can be considered one version of a land-use suitability assessment. Other work in New Zealand has focused on land-use suitability with regard to impacts on catchment water quality. 

- **Land tenure**: ways of holding land (e.g. fee simple, customary title, leasehold, life estate). Related information, such as whether the land is owner-occupied, may be captured in a classification system for land tenure, which may be valuable information alongside land use. Whether land is publicly owned is often an important dimension of a hierarchical classification of land use but strictly relates to land tenure. 

- **Land value**: the fiscal value of the land, which in New Zealand is formally defined in the Ratings Valuation Act 1998. The ‘value of improvements’ specifically relates to the added value that improvements give to land. Improvements in relation to land refers to all work done on, or material used on or for the benefit of, land by the expenditure of capital or labour. 

---

## References

[^1]: Sahr K, White D, Kimerling AJ 2003. Geodesic discrete global grid systems. Cartography and Geographic Information Science 30.2: 121–134. 

[^2]: Law R, Ardo J 2023. Northland Regional Council land-use classification: methodological report. Manaaki Whenua – Landcare Research contract report LC4345 for Northland Regional Council. 

[^3]: Lynn I, Manderson A, Page M, Harmsworth G, Eyles G, Douglas G, et al. 2009. Land use capability survey handbook: A New Zealand handbook for the classification of land (3rd edn). Hamilton, AgResearch; Lincoln, Landcare Research; Lower Hutt, GNS Science. 