FROM continuumio/anaconda

ADD . /app
RUN apt update \
    && apt install -y \
    build-essential \
    nginx

RUN mkdir /data /meta /whoosh
WORKDIR /app
RUN conda update conda -y \
    && conda env create -f environment.yml
ENV PATH /opt/conda/envs/ave2/bin:$PATH
RUN python setup.py develop
RUN cp settings.docker.cfg settings.cfg
RUN cp nginx.conf /etc/nginx/sites-enabled/default

RUN cd /var/www/html && curl -L 'https://bintray.com/nlesc-ave/ave/download_file?file_path=ave-app-latest.tar.bz2' | tar -jxf -

WORKDIR /app
CMD service nginx start && avedata run

VOLUME /data
VOLUME /meta
VOLUME /whoosh
EXPOSE 80
