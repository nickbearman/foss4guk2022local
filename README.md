# FOSS4G:UK 2022 Local

## Using the OS Data Hub to automate Open Data ETL to open source databases

### Introduction

[OS OpenData Downloads](https://osdatahub.os.uk/downloads/open) is a set of free, downloadable digital maps and comprehensive data of Great Britain, available for anyone to use, for any purpose.

The [OS Downloads API](https://osdatahub.os.uk/docs/downloads/overview) is a service that lets you automate the discovery and download of OS OpenData and data packages.

The scripts included in this repository will allow you to:

1. Connect to the OS Downloads API and return a listing of the available Open Data products.
2. Download a product (in the format) of your choosing.
3. Extract and load the data into a spatially-enabled database.

### Requirements

- [Jupyter Notebook](https://jupyter.org/) => Tool for interactively developing and presenting data science projects.
- [PostgreSQL](https://www.postgresql.org/) => An open-source relational database management system (RDBMS).
- [PostGIS](https://postgis.net/) => Spatial database extender for PostgreSQL object-relational database.
- [Geospatial Data Abstraction Library (GDAL)](https://gdal.org/index.html) => Translator library released by the Open Source Geospatial Foundation for reading/writing raster and vector geospatial data formats.

### Licence

The contents of this repository are licensed under the [Open Government Licence 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/).

![Logo](http://www.nationalarchives.gov.uk/images/infoman/ogl-symbol-41px-retina-black.png "OGL logo")
