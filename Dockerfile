FROM python:3.7-alpine

RUN pip install --no-cache-dir pipenv && \
    apk add --update --no-cache git build-base

WORKDIR /opt/azafea-metrics-proxy/src

COPY Pipfile.lock .

RUN pipenv install --ignore-pipfile

COPY . .

ENTRYPOINT ["pipenv", "run", "proxy"]

EXPOSE 8080

HEALTHCHECK CMD wget --spider --quiet http://localhost:8080/ --user-agent 'Healthcheck' || exit 1
