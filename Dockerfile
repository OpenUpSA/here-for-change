FROM openup/docker-python-nodejs:python3.9-nodejs12

ENV POETRY_VIRTUALENVS_CREATE false
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV NODE_ENV production

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -

RUN set -ex; \
  apt-get update; \
  # dependencies for building Python packages \
  apt-get install -y build-essential python3.7-dev; \
  # psycopg2 dependencies \
  apt-get install -y libpq-dev; \
  # postgis dependencies view dependencies here: https://postgis.net/docs/postgis_installation.html#install_requirements \
  apt-get install -y proj-bin; \
  apt-get install -y binutils; \
  apt-get install -y libgeos++-dev libgeos-c1v5 libgeos-dev;\
  apt-get install -y postgresql;\
  # git for codecov file listing \
  apt-get install -y git; \
  # cleaning up unused files \
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
  rm -rf /var/lib/apt/lists/*

RUN pip install -U poetry

# Copy, then install requirements before copying rest for a requirements cache layer.
COPY pyproject.toml poetry.lock /tmp/
RUN set -ex; \
  cd /tmp; \
  poetry install

COPY . /app

WORKDIR /app



RUN set -ex; \
  yarn; \
  yarn build



#INSTALL GDAL [postgis dependency]
RUN add-apt-repository ppa:ubuntugis/ppa;\
    apt-get -y update;\
    apt-get -y install gdal-bin;\
    apt-get -y install libgdal-dev;\
    export CPLUS_INCLUDE_PATH=/usr/include/gdal\
    export C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get -y install postgis;



EXPOSE 5000
CMD /app/bin/start.sh
