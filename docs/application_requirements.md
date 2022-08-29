# DCR-CORE - Application - Requirements

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)

The required software is listed below. 
Regarding the corresponding software versions, you will find the detailed information in the [Release Notes](https://konnexionsgmbh.github.io/dcr-core/release_notes). 

## 1. Operating System

Continuous delivery / integration (CD/CI) runs on **`Ubuntu`** and development is done with **`Windows 10`**.
For the Windows operating systems, only additional the functionality of the **`grep`**, **`make`**  and **`sed`** tools must be made available, e.g. via [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"}, [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} or [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}.

## 2. [Pandoc](https://pandoc.org){:target="_blank"} & [TeX Live](https://www.tug.org/texlive){:target="_blank"}

To convert the non-PDF documents into **`pdf`** files for [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} processing, 
the universal document converter [Pandoc](https://pandoc.org){:target="_blank"} 
and the TeX typesetting system [TeX Live](https://www.tug.org/texlive){:target="_blank"} are used and must therefore also be installed.
The installation of the [TeX Live](https://www.tug.org/texlive){:target="_blank"} Frontend is not required.

## 3. [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"}

The software library [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} is used to tokenize the **`pdf`** documents. 
**DCR-CORE** contains the free version of [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"}. 
This free version is limited to files with a maximum size of 1 MB and a maximum number of pages of 10. 
If larger files are to be processed, a licence must be purchased from [PDFlib GmbH](https://www.pdflib.com){:target="_blank"}. 
Details on the conditions can be found [here](https://www.pdflib.com/buy/){:target="_blank"}.

## 4. [Poppler](https://poppler.freedesktop.org){:target="_blank"}

To convert the scanned PDF documents into image files for Tesseract OCR, the rendering library [Poppler](https://poppler.freedesktop.org){:target="_blank"} is used and must therefore also be installed.

## 5. Python

Because of the use of the new typing features, [Python](https://docs.python.org/3/whatsnew/3.10.html){:target="_blank"} is required.

## 6. [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}

To convert image files into **`pdf`** files, [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} is required.

