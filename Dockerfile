FROM python:3.8.11-slim-buster

ENV PYCURL_SSL_LIBRARY=nss

RUN apt update --fix-missing
RUN apt install -y build-essential \
    ca-certificates \
    curl \
    gettext \
    git \
    gunicorn \
    libbz2-dev \
    libcairo2 \
    libcurl4-openssl-dev \
    libffi-dev \
    liblzma-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libreadline-dev \
    libsqlite3-dev \
    libpcre3 \
    libpcre3-dev \
    llvm \
    make  \
    net-tools \
    nginx \
    openssl \
    python3-dev \
    postgresql-client \
    shared-mime-info \
    redis-server \
    wget \
    zlib1g-dev

RUN apt-get install -y --no-install-recommends libcurl4-nss-dev libssl-dev

## Add the cart user
RUN useradd -rm -d /home/cart -s /bin/bash -g root -G sudo -u 1001 cart

# Set DJANGO_MODULE_SETTINGS environment variable
ENV DJANGO_SETTINGS_MODULE=cart_api.settings

# Create a virtual env
RUN python -m venv /opt/app/env
ENV PATH /opt/app/env/bin:$PATH

# Activate the VEnv and install requirements
ADD requirements /requirements
RUN . /opt/app/env/bin/activate
RUN /opt/app/env/bin/pip install -r /requirements/production.txt


# Create a copy of the repository to /opt/app
COPY . /opt/app

# Create Logs folder
RUN mkdir -p /opt/app/logs
RUN chown -R www-data /opt/app/logs
RUN chmod 777 /opt/app/logs

# Add the nginx settings
RUN mkdir -p /tmp/assets-cache/tmp

COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./conf/fastcgi_params /etc/nginx/fastcgi_params
COPY ./conf/nginx_vhost.conf /etc/nginx/conf.d/default.conf
COPY ./conf/logrotate /etc/logrotate.d/nginx


# Set the as path to work on
WORKDIR /opt/app

# Run Migrations and Start Gunicorn
COPY start.sh /

EXPOSE 80
EXPOSE 8000

