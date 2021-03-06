FROM python:3.7-alpine

RUN pip install --no-cache-dir pipenv template && \
    apk add --update --no-cache git build-base

RUN adduser --system --shell /sbin/nologin --home /opt/azafea-metrics-proxy azafea && \
    install -d -m 755 -o azafea /opt/azafea-metrics-proxy/src
USER azafea
WORKDIR /opt/azafea-metrics-proxy/src

COPY Pipfile.lock .

RUN pipenv install --ignore-pipfile --dev

COPY . .

ENTRYPOINT ["./entrypoint", "pipenv", "run"]

CMD ["proxy", "-c", "/tmp/config.toml", "run"]

ENV VERBOSE=false
ENV REDIS_HOST=localhost
ENV REDIS_PASSWORD="CHANGE ME!!"

EXPOSE 8080

HEALTHCHECK CMD wget --spider --quiet http://localhost:8080/ --user-agent 'Healthcheck' || exit 1
