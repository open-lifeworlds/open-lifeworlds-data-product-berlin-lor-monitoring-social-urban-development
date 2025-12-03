
# Data Product Canvas - Berlin Monitoring Social Urban Development

## Metadata

* owner: Open Lifeworlds
* description: Data product providing Berlin monitoring social urban development data on different hierarchy levels
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development
* license: CC-BY 4.0
* updated: 2025-11-09

## Input Ports

### berlin-lor-geodata

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-lor-geodata/refs/heads/main/data-product-manifest.yml

### berlin-monitoring-social-urban-development-aligned

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-monitoring-social-urban-development-source-aligned/refs/heads/main/data-product-manifest.yml

## Transformation Steps

* [Data extractor](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/extract/data_extractor.py) extracts data from inout ports
* [Data blender](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/transform/data_blender.py) blends csv data into geojson files

## Output Ports

### berlin-monitoring-social-urban-development-geojson
name: Berlin Monitoring Social Urban Development Geojson
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/tree/main/data/03-gold/berlin-monitoring-social-urban-development-geojson
* license: CC-BY 4.0
* updated: 2025-11-09

**Files**

* [berlin-monitoring-social-urban-development-2013-00-district-regions.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2013-00-district-regions.geojson)
* [berlin-monitoring-social-urban-development-2013-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2013-00-districts.geojson)
* [berlin-monitoring-social-urban-development-2013-00-planning-areas.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2013-00-planning-areas.geojson)
* [berlin-monitoring-social-urban-development-2015-00-district-regions.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2015-00-district-regions.geojson)
* [berlin-monitoring-social-urban-development-2015-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2015-00-districts.geojson)
* [berlin-monitoring-social-urban-development-2015-00-planning-areas.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2015-00-planning-areas.geojson)
* [berlin-monitoring-social-urban-development-2017-00-district-regions.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2017-00-district-regions.geojson)
* [berlin-monitoring-social-urban-development-2017-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2017-00-districts.geojson)
* [berlin-monitoring-social-urban-development-2017-00-planning-areas.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2017-00-planning-areas.geojson)
* [berlin-monitoring-social-urban-development-2019-00-district-regions.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2019-00-district-regions.geojson)
* [berlin-monitoring-social-urban-development-2019-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2019-00-districts.geojson)
* [berlin-monitoring-social-urban-development-2019-00-planning-areas.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2019-00-planning-areas.geojson)
* [berlin-monitoring-social-urban-development-2021-00-district-regions.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2021-00-district-regions.geojson)
* [berlin-monitoring-social-urban-development-2021-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2021-00-districts.geojson)
* [berlin-monitoring-social-urban-development-2021-00-planning-areas.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-geojson/berlin-monitoring-social-urban-development-2021-00-planning-areas.geojson)


### berlin-monitoring-social-urban-development-statistics
name: Berlin Monitoring Social Urban Development Statistics
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/tree/main/data/03-gold/berlin-monitoring-social-urban-development-statistics
* license: CC-BY 4.0
* updated: 2025-11-09

**Files**

* [berlin-monitoring-social-urban-development-statistics.json](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-monitoring-social-urban-development/refs/heads/main/data/03-gold/berlin-monitoring-social-urban-development-statistics/berlin-monitoring-social-urban-development-statistics.json)


## Observability

### Quality metrics

 * name: geojson_property_completeness
 * description: The percentage of geojson features that have all necessary properties

| Name | Value |
| --- | --- |
| berlin-monitoring-social-urban-development-2013-00-districts.geojson | 100 |
| berlin-monitoring-social-urban-development-2013-00-district-regions.geojson | 100 |
| berlin-monitoring-social-urban-development-2013-00-planning-areas.geojson | 100 |
| berlin-monitoring-social-urban-development-2015-00-districts.geojson | 100 |
| berlin-monitoring-social-urban-development-2015-00-district-regions.geojson | 100 |
| berlin-monitoring-social-urban-development-2015-00-planning-areas.geojson | 100 |
| berlin-monitoring-social-urban-development-2017-00-districts.geojson | 67 |
| berlin-monitoring-social-urban-development-2017-00-district-regions.geojson | 0 |
| berlin-monitoring-social-urban-development-2017-00-planning-areas.geojson | 100 |
| berlin-monitoring-social-urban-development-2019-00-districts.geojson | 42 |
| berlin-monitoring-social-urban-development-2019-00-district-regions.geojson | 1 |
| berlin-monitoring-social-urban-development-2019-00-planning-areas.geojson | 66 |
| berlin-monitoring-social-urban-development-2021-00-districts.geojson | 33 |
| berlin-monitoring-social-urban-development-2021-00-district-regions.geojson | 0 |
| berlin-monitoring-social-urban-development-2021-00-planning-areas.geojson | 39 |


## Classification

**The nature of the exposed data (source-aligned, aggregate, consumer-aligned)**

consumer-aligned


---
This data product canvas uses the template of [datamesh-architecture.com](https://www.datamesh-architecture.com/data-product-canvas).