FROM python:3.13
LABEL authors='shyin.lim'

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /web
WORKDIR /web

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Taipei

EXPOSE 8787

CMD python /web/main_project/manage.py runserver 0.0.0.0:8787