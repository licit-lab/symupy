FROM continuumio/miniconda3:4.8.3-alpine

# User 
USER root

# Open ports
EXPOSE 5000

# Add bash 
RUN apk add --no-cache bash

# Add PATH
ENV PATH /opt/conda/bin/:$PATH

# Install env
RUN ["bash","-c","conda create -n symupy -c conda-forge -c licit-lab jupyterlab symupy"]
