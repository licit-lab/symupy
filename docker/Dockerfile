FROM continuumio/miniconda3:4.8.3-alpine

# User
USER root

# Open ports
EXPOSE 5000

# Add bash
RUN apk add --no-cache bash

# Add PATH
ENV PATH /opt/conda/bin/:$PATH

# Create env
COPY conda/env.yaml requirements.dev.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/env.yaml" ]; then /opt/conda/bin/conda env create -f /tmp/conda-tmp/env.yaml; fi

# Activate + dev-tools
RUN source activate symupy\
    && pip install -r /tmp/conda-tmp/requirements.dev.txt\
    && rm -rf /tmp/conda-tmp

# Install env
# RUN ["bash","-c","conda create -n symupy -c conda-forge -c licit-lab jupyterlab symupy"]
