FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y apache2 libapache2-mod-wsgi-py3 python3 python3-pip python3-dev python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m venv env

COPY . /app/REDSOCIAL_ATI-DJANGO/

COPY requirements.txt /app/REDSOCIAL_ATI-DJANGO/
RUN /app/env/bin/pip install -r /app/REDSOCIAL_ATI-DJANGO/requirements.txt

RUN /app/env/bin/python3 -c "import django; print('Django version:', django.get_version())"

COPY apache-chati.conf /etc/apache2/sites-available/000-default.conf

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

CMD ["/usr/local/bin/start.sh"]