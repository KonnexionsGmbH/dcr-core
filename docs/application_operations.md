# DCR-CORE - Application - Operations

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)

The details of the method call `document` can be found in the API documentation.

## 1. Use as a library

The following sample code extracts the content structure of the pdf file `1910.03678.pdf` into a JSON file:

    from dcr_core import cls_process

    process = cls_process.Process()
    process.document("data/inbox_prod/1910.03678.pdf")

## 2. Use of a Docker container

The following steps extract the content structure of document `1910.03678.pdf` using Docker Container.

**1. Restarting the container:**

    docker start dcr-core

**2. Starting Python in the Virtual Environment (inside the `dcr-core` container):**

    python3 -m pipenv run python3

**3. Make the `dcr_core` module available:**

    from dcr_core import cls_process

**4. Create an instance of the `Process` class:**

    process = cls_process.Process()

**5. Process document files:**

    process.document("data/inbox_prod/1910.03678.pdf")
