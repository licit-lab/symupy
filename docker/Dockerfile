FROM continuumio/miniconda3:4.8.3-alpine

# User 
USER root

# Open ports
EXPOSE 5000

# Add bash 
RUN apk add --no-cache bash

# Add PATH
ENV PATH /opt/conda/bin/:$PATH

COPY conda/env.yaml /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/env.yaml" ]; then /opt/conda/bin/conda env create -f /tmp/conda-tmp/env.yaml; fi \
    && rm -rf /tmp/conda-tmp

# Install env
# RUN ["bash","-c","conda create -n symupy -c conda-forge -c licit-lab jupyterlab symupy"]
