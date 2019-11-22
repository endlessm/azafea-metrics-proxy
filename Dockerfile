FROM ubuntu:disco

ENV LANG C.UTF-8

WORKDIR /opt/azafea-metrics-proxy/src

COPY Pipfile.lock .

RUN apt --quiet --assume-yes update \
    && apt --quiet --assume-yes --no-install-recommends install \
        gcc \
        python3 \
        python3-dev \
        python3-pip \
    && pip3 install pipenv \
    && pipenv install --ignore-pipfile \
    && apt --quiet --assume-yes autoremove --purge \
        gcc \
        python3-dev \
    && rm -rf /var/cache/{apt,debconf} /var/lib/apt/lists/* /var/log/{apt,dpkg.log}

COPY . .

ENTRYPOINT ["pipenv", "run", "proxy"]
