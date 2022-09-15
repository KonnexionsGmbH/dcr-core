# Ubuntu 20.04 Focal Fossa
FROM python:3.10.6 as base

COPY LICENSE Pipfile Pipfile.lock logging_cfg.yaml MANIFEST.in Makefile pyproject.toml setup.cfg setup.cfg.reference /dcr-core/
COPY data/ /dcr-core/data/
COPY src/ /dcr-core/src/
COPY scripts/ /dcr-core/scripts/
COPY tests/ /dcr-core/tests/

RUN ls -alF /dcr-core/

LABEL maintainer="Konnexions GmbH"


# Setting Environment Variables ----------------------------------------------------
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=false
ARG DEBIAN_FRONTEND=noninteractive
ARG LOCALE=en_US.UTF-8
ARG TIMEZONE=Europe/Zurich

# ARG VERSION_OPENSSL=1_1_1o
# ARG VERSION_PANDOC=2.19.2
# ARG VERSION_POPPLER=22.02.0

ENV PYTHONUNBUFFERED=1

ENV VERSION_DCR-CORE=0.9.7

SHELL ["/bin/bash", "-c"]

RUN echo "--------------------------------------------------------------------------" \
 && echo "Step: Supplement necessary system software" \
 && echo "--------------------------------------------------------------------------" \
 && apt-get update -qy \
 && apt-get install -qy software-properties-common tesseract-ocr poppler-utils pandoc \
 && pip install --upgrade pip pipenv \
 && pandoc -v \
 && pdftocairo -v \
 && tesseract --version \
 && tesseract --list-langs \
 && python --version \
 && pip --version \
 && pipenv --version

ENV PATH="/root/.local/bin:${PATH}"

ENV PYTHONPATH=${PYTHONPATH}:/dcr-core/src:/dcr-core/src/dcr_core

RUN echo "--------------------------------------------------------------------------" \
 && echo "Step: dcr-core" \
 && echo "--------------------------------------------------------------------------" \
 && cd /dcr-core \
 && pipenv install \
 && pipenv run spacy download en_core_web_trf \
 && pipenv run pip freeze

RUN echo "--------------------------------------------------------------------------" \
 && echo "Step: Cleanup" \
 && echo "--------------------------------------------------------------------------" \
 && apt-get -qy autoclean \
 && apt-get -qy autoremove \
 && rm -rf /tmp/*

FROM python:3.10.6
COPY --from=base / /

ENV DCR_ENVIRONMENT_TYPE=prod

WORKDIR /dcr-core

CMD ["/bin/bash"]
