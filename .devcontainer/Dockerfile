# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.158.0/containers/python-3-miniconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# Add bash
# RUN apk add --no-cache bash

# Add PATH
ENV PATH /opt/conda/bin/:$PATH

# Copy environment.yml + requirements.dev.txt
COPY docs/environment.doc.yaml requirements.dev.txt /workspaces/symupy/

RUN if [ -f "/workspaces/symupy/environment.doc.yaml" ]; then /opt/conda/bin/conda env create -f /workspaces/symupy/environment.doc.yaml; fi

# Activate + dev-tools
RUN /bin/bash -c conda activate symupy\
    && pip install -r /workspaces/symupy/requirements.dev.txt\
    && rm -rf /workspaces/symupy/

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends build-essential