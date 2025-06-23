# Base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH

# Install system and R dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    nano \
    build-essential \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    python3 \
    python3-pip \
    r-base \
    && apt-get clean

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    conda clean -afy

# Configure Conda channels
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict

# Install bioinformatics tools and Python dependencies
RUN conda install -y \
    fastqc \
    trimmomatic \
    fastp \
    bwa \
    samtools \
    multiqc \
    megahit \
    krona \
    prokka \
    pandas \
    numpy \
    matplotlib && \
    conda clean -afy

# Link Krona manually (if needed)
RUN ln -s /opt/conda/bin/ktImportText /usr/local/bin/ktImportText || true

# Install R packages and MelonnPan
RUN R -e "install.packages(c('devtools', 'optparse', 'data.table', 'doParallel', 'foreach', 'ggplot2', 'MatrixStats', 'ROCR', 'pheatmap'), repos='https://cloud.r-project.org')" && \
    R -e "if (!requireNamespace('BiocManager', quietly = TRUE)) install.packages('BiocManager', repos='https://cloud.r-project.org')" && \
    R -e "BiocManager::install('AssocTests')" && \
    R -e "devtools::install_github('biobakery/melonnpan')"

# Set up default working directories
WORKDIR /pipeline
WORKDIR /data

# Default command
CMD ["bash"]

