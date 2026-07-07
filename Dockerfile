FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    UV_PYTHON_PREFERENCE=only-system

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    lmodern \
    texlive-fonts-recommended \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-pictures \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /workspace
