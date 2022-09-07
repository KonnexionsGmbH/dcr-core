# DCR-CORE - Application - Installation

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)

## 1. Use as a library

**`DCR-CORE`** is installable using the package manager [PyPI](https://pypi.org). 
Your package manager will find a version that works with your interpreter. 

Example installation with `pip`:

      pip install dcr-core

## 2. Use of a Docker container

A fully functional Docker image is available [here](https://hub.docker.com/repository/docker/konnexionsgmbh/dcr-core) on DockerHub. 
From this, a local Docker container can be created with the following command:

    docker run -it --name dcr-core -v <local directory>:/dcr-core/data/inbox_prod konnexionsgmbh/dcr-core:0.9.7

`<local directory>` is the local directory where the files created during the processing are stored.
In addition to the software listed under prerequisites, the Docker container also contains a complete virtual environment for running **`DCR-CORE`** in suitable versions.