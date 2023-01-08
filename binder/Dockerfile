# c.f. https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html#preparing-your-dockerfile
FROM python:3.10-slim-bullseye

# Add default user NB_USER
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

USER root
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
USER ${NB_USER}

# Set PATH to pickup virtualenv by default
ENV PATH=/usr/local/venv/bin:"${PATH}"
# Make sure the contents of the repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME} && \
    python -m venv /usr/local/venv && \
    chown -R ${NB_UID} /usr/local/venv
USER ${NB_USER}
WORKDIR ${HOME}

# Install necessary jupyter dependencies
# Install jupyterhub to allow use of the repository with an authenticated Binder

# Using lock file for reproducibility of issue
# RUN python -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
#     python -m pip --no-cache-dir install jupyter jupyterlab jupyterhub && \
#     command -v python && \
#     python -m pip list
COPY requirements.txt /docker/requirements.txt
COPY requirements.lock /docker/requirements.lock
RUN python -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
    python -m pip --no-cache-dir install \
        --no-deps \
        --require-hashes \
        --requirement /docker/requirements.lock && \
    command -v python && \
    python -m pip list
