FROM continuumio/miniconda:latest

RUN apt-get update && \
    apt-get -y install gcc mono-mcs libz-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin:$PATH"
ENV PATH="/opt/conda/bin:$PATH"
RUN conda config --add channels defaults && \
    conda config --add channels anaconda && \
    conda config --add channels bioconda && \
    conda config --set always_yes yes --set changeps1 no && \
    conda install -c bioconda python=3.6 cython numpy \
                    networkx seaborn pyBigwig six pysam \
                    ujson pytest scipy matplotlib samtools \
                    future pytest-cov codecov && \
    conda clean -afy

COPY . /opt/sequencing_tools

RUN cd /opt/sequencing_tools &&\
     pip install .
ENV PATH="/opt/conda/bin:${PATH}"
ENTRYPOINT ["/opt/conda/bin/seqtools"]
CMD ["--help"]
