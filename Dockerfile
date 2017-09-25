FROM continuumio/miniconda3

RUN apt-get update \
    && apt-get install -y \
    nginx && \
    mkdir /data /meta /whoosh

WORKDIR /app

ADD environment.yml /app/environment.yml

ENV PATH /opt/conda/envs/ave2/bin:$PATH

RUN conda update conda -y && \
    conda env create -f environment.yml && \
    # Anaconda twoBitInfo, twoBitToFa and bigBedInfo can not handle https, download latest binary from source
    curl -o /opt/conda/envs/ave2/bin/twoBitInfo http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/twoBitInfo && \
    chmod +x /opt/conda/envs/ave2/bin/twoBitInfo && \
    curl -o /opt/conda/envs/ave2/bin/twoBitToFa http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/twoBitToFa && \
    chmod +x /opt/conda/envs/ave2/bin/twoBitToFa && \
    curl -o /opt/conda/envs/ave2/bin/bigBedInfo http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bigBedInfo && \
    chmod +x /opt/conda/envs/ave2/bin/bigBedInfo

ADD . /app

RUN python setup.py install && \
    cp settings.docker.cfg settings.cfg && \
    cp nginx.conf /etc/nginx/sites-enabled/default && \
    cd /var/www/html && \
    curl -L 'https://bintray.com/nlesc-ave/ave/download_file?file_path=ave-app-latest.tar.bz2' | tar -jxf -

CMD service nginx start && gunicorn -w 4 --threads 2 -t 60 -b 127.0.0.1:8080 avedata.app:app

VOLUME /data /meta /whoosh
EXPOSE 80
