FROM continuumio/anaconda

RUN apt update \
    && apt install -y \
    build-essential \
    nginx

RUN mkdir /data /meta /whoosh
ADD environment.yml /app/environment.yml
WORKDIR /app
RUN conda update conda -y \
    && conda env create -f environment.yml
ENV PATH /opt/conda/envs/ave2/bin:$PATH
ADD . /app
RUN python setup.py develop
RUN cp settings.docker.cfg settings.cfg
ADD nginx.conf /etc/nginx/sites-enabled/default

RUN cd /var/www/html && curl -L 'https://bintray.com/nlesc-ave/ave/download_file?file_path=ave-app-latest.tar.bz2' | tar -jxf -

WORKDIR /app
CMD service nginx start && gunicorn -w 4 --threads 2 -t 60 avedata.avedata:app

VOLUME /data
VOLUME /meta
VOLUME /whoosh
EXPOSE 80