# New Zealand Standard Land Use Classification System

Status: Draft
Version: 0.1
Developed by: Manaaki Whenua – Landcare Research

## Overview

The NZSLUCS is intended for the purpose of environmental monitoring, especially fresh water. Land use practices are of particular relevance to this classification system, as there is a need to understand social and economic capacity for changes to land management practices.

Land management practices are incorporated when needed to distinguish between land uses.

## Geographic scale

The intended geographic unit of this classification system is the property parcel. However it may be appropriate to map sub-parcel geographic entities for particular classes, particularly if the boundary of natural features (forests, waterways) is pertinent, or if the parcel is very large. Additionally, whether sub-parcel classification is appropriate may depend on the geographic scale of available input data. Mapping sub-parcel areas is therefore left to operator discretion.

Regardless, property parcel identification, and boundaries, should be present in output land use data.

## Data specifications

### Data format and spatial referencing

Vector data format: [GeoPackage](https://www.geopackage.org/) v1.4.0 or later and/or [GeoParquet](https://geoparquet.org/) v1.0.0 or later.

Raster data (or other formats) may be produced for user convenience, but no particular format is specified. Vector data is mandatory.

Coordinate system: any [current official projection](https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/projections) may be used:

- New Zealand Transverse Mercator 2000 (NZTM2000).
- NZGD meridional circuits (e.g. for regional extracts) or offshore island projections.
- New Zealand Continental Shelf Lambert Conformal 2000 (NZCS2000).