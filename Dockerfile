# Base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH

# Install system utilities and Python dependencies
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
    python3 \
    python3-pip \
    python3-matplotlib \
    python3-pandas \
    python3-numpy \
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

# Install bioinformatics tools via Conda
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

# Create pipeline working directory
WORKDIR /pipeline

# Set default working directory when container runs
WORKDIR /data

# Set default command
CMD ["bash"]

