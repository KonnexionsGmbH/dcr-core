# DCR-CORE - Document Content Recognition API - README

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr-core.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr-core/0.9.7)

Based on the paper "Unfolding the Structure of a Document using Deep Learning" (**[Rahman and Finin, 2019](https://arxiv.org/abs/1910.03678)**), this software project aims to use various software techniques to automatically detect the structure in arbitrary **`pdf`** documents and thus make these documents more searchable.

The computer linguistic methods used here assume that the documents to be processed are in **`pdf`** format.
However, in order to be flexible in the selection of documents with respect to file format, **`DCR-CORE`** includes a sophisticated preprocessor mechanism that can convert many of the non **`pdf`** formats to **`pdf`** format.

From the documents in **`pdf`** format, the next steps extract the text with the relevant metadata word by word, line by line, or page by page. In line-by-line extraction, an attempt is made to classify the individual lines and mark them accordingly, so that these line classifications can later be taken into account in token generation.

In the currently last step qualified tokens can be generated, which contain on the one hand information about the localization of the token in the document and on the other hand token classification features like lemma, form, normalization etc..

Please see the **[Documentation](https://konnexionsgmbh.github.io/dcr-core)** for more detailed information.

## 1. Features

### 1.1 General 
 
- Support for documents in different languages - English as standard.

### 1.2 Preprocessor 

- Identification of scanned **`pdf`** documents with [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html).
- Conversion of the scanned **`pdf`** documents into a set of **`jpeg`** or **`png`** files with [pdf2image](https://pypi.org/project/pdf2image) and [Poppler](https://poppler.freedesktop.org).
- Conversion of the documents of type **`bmp`**, **`gif`**, **`jp2`**, **`jpeg`**, **`png`**, **`pnm`**, **`tif`**, **`tiff`** or **`webp`** to **`pdf`** format with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
- Conversion of **`csv`**, **`docx`**, **`epub`**, **`html`**, **`odt`**, **`rst`** or **`rtf`** type documents to **`pdf`** format with [Pandoc](https://pandoc.org) and [TeX Live](https://www.tug.org/texlive).

### 1.3 Natural Language Processing (NLP) 

- Extract text and metadata from **`pdf`** documents with [PDFlib TET](https://www.pdflib.com/products/tet/).
- Classification of lines in the document, e.g. body, footer, header lines, etc.
- Sentence-by-sentence determination of the token structure using [spaCy](https://spacy.io).
- Storage of the analysis results in JSON and XML flat files.

## 2 Quick start

### 2.1 Requirements



### 2.2 Installation


### 2.3 Running an example file


### 2.4 Resulting files


Want to try it out but don't want to install anything ? We have set up a [Google Colab](https://colab.research.google.com/github/deezer/spleeter/blob/master/spleeter.ipynb).

Ready to dig into it ? In a few lines you can install **Spleeter**  and separate the vocal and accompaniment parts from an example audio file.
You need first to install `ffmpeg` and `libsndfile`. It can be done on most platform using [Conda](https://github.com/deezer/spleeter/wiki/1.-Installation#using-conda):

```bash
# install dependencies using conda
conda install -c conda-forge ffmpeg libsndfile
# install spleeter with pip
pip install spleeter
# download an example audio file (if you don't have wget, use another tool for downloading)
wget https://github.com/deezer/spleeter/raw/master/audio_example.mp3
# separate the example audio into two components
spleeter separate -p spleeter:2stems -o output audio_example.mp3
```

> :warning: Note that we no longer recommend using `conda` for installing spleeter.

> ⚠️ There are known issues with Apple M1 chips, mostly due to TensorFlow compatibility. Until these are fixed, you can use [this workaround](https://github.com/deezer/spleeter/issues/607#issuecomment-1021669444).

You should get two separated audio files (`vocals.wav` and `accompaniment.wav`) in the `output/audio_example` folder.

For a detailed documentation, please check the [repository wiki](https://github.com/deezer/spleeter/wiki/1.-Installation)

## Development and Testing

This project is managed using [Poetry](https://python-poetry.org/docs/basic-usage/), to run test suite you
can execute the following set of commands:

```bash
# Clone spleeter repository
git clone https://github.com/Deezer/spleeter && cd spleeter
# Install poetry
pip install poetry
# Install spleeter dependencies
poetry install
# Run unit test suite
poetry run pytest tests/
```

## 3. Directory and File Structure of this Repository

### 3.1 Directories

| Directory         | Content                                                               |
|-------------------|-----------------------------------------------------------------------|
| .github/workflows | [GitHub Action](https://github.com/actions) workflows.                |
| PDFlib            | Python package of [PDFlib TET](https://www.pdflib.com/products/tet/). |
| data              | Example rule files for document line classification.                  |
| dcr_core          | Python package.                                                       |
| docs              | **`DCR-CORE`** documentation files.                                     |
| tests             | Scripts and data for pytest.                                          |

### 3.2 Files

| File             | Functionality                                                                                              |
|------------------|------------------------------------------------------------------------------------------------------------|
| .gitignore       | Configuration of files and folders to be ignored.                                                          |
| .pylintrc        | Configuration file for [pylint](https://github.com/PyCQA/pylint).                                          |
| LICENSE          | Text of the licence terms.                                                                                 |
| logging_cfg.yaml | Configuration of the Logger functionality.                                                                 |
| Makefile         | Definition of tasks to be excuted with the `make` command.                                                 |
| MANIFEST.in      | Source distribution commands for [PyPA](https://packaging.python.org/en/latest/guides/using-manifest-in/). |
| mkdocs.yml       | Configuration file for [MkDocs](https://github.com/mkdocs/mkdocs/).                                        |
| Pipfile          | Definition of the Python package requirements.                                                             |
| Pipfile.lock     | Definition of the specific versions of the Python packages.                                                |
| pyproject.toml   | Build system requirements according to [PEP 518](https://peps.python.org/pep-0518/).                       |
| README.md        | This file.                                                                                                 |
| setup.cfg        | Setup configuration file - [see here](https://setuptools.pypa.io/en/latest/setuptools.html).               |

## 4. Support

If you need help with **`DCR-CORE`**, do not hesitate to get in contact with us!

- For questions and high-level discussions, use **[Discussions](https://github.com/KonnexionsGmbH/dcr-core/discussions)** on GitHub.
- To report a bug or make a feature request, open an **[Issue](https://github.com/KonnexionsGmbH/dcr-core/issues)** on GitHub.

Please note that we may only provide support for problems / questions regarding core features of **`DCR-CORE`**.
Any questions or bug reports about features of third-party themes, plugins, extensions or similar should be made to their respective projects. 
But, such questions are **not** banned from the **[Discussions](https://github.com/KonnexionsGmbH/dcr-core/discussions)**.

Make sure to stick around to answer some questions as well!

## 5. Links

- **[Official Documentation](https://konnexionsgmbh.github.io/dcr-core)**
- **[Release Notes](https://konnexionsgmbh.github.io/dcr-core/release_notes)**
- **[Discussions](https://github.com/KonnexionsGmbH/dcr-core/discussions)** (Third-party themes, recipes, plugins and more)

## 6. Contributing to DCR

The **`DCR-CORE`** project welcomes, and depends on, contributions from developers and users in the open source community. 
Please see the **[Contributing Guide](https://konnexionsgmbh.github.io/dcr-core/contributing)** for
information on how you can help.

## 7. Code of Conduct

Everyone who interacts in the **`DCR-CORE`** project's codebase, issue trackers, and discussion forums is expected to follow the **[Code of Conduct](https://konnexionsgmbh.github.io/dcr-core/code_of_conduct)**.

## 8. License

**[Konnexions Public License (KX-PL)](https://konnexionsgmbh.github.io/dcr-core/license)**
