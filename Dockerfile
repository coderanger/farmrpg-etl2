
FROM python:3.11 AS build

# On big cloud machines, we hit connection limits.
ENV POETRY_INSTALLER_MAX_WORKERS 8

WORKDIR /src

RUN curl -o /install-poetry.py https://install.python-poetry.org && \
    python /install-poetry.py && \
    python -m venv .venv

COPY . /src/
RUN /root/.local/bin/poetry install --without=dev && \
    .venv/bin/python manage.py collectstatic

FROM python:3.11
ENV PATH "/src/.venv/bin:${PATH}"
# COPY doesn't bring over the xattrs for this so it can't be in the build image.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libcap2-bin && \
    setcap 'cap_net_bind_service=+ep' /usr/local/bin/python3.11 && \
    apt-get purge -y libcap2-bin && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
COPY --from=build /src /src
WORKDIR /src
USER 65534
