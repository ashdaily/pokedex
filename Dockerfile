FROM ubuntu:20.10

# Motivated by 12 factor app ideology, we want to keep docker images
# similar for different environments like local, development, testing, staging & production.
# So, it's better to have one Dockerfile for different environments.
# TARGET_ENV is used to help us distinguish between different environments like
# local, development, testing, staging, production. By default, TARGET_ENV is
# set to "local". To build docker image with other environments use the docker command:
# `docker build --build-arg TARGET_ENV=production`
ARG TARGET_ENV=local
ENV TARGET_ENV=$TARGET_ENV

# which python version to install
ENV PYTHON_VERSION=3.9

RUN apt update --yes
RUN apt install --yes software-properties-common

# for postgres to use
RUN apt install --yes libpq-dev python${PYTHON_VERSION}-dev

# need to update ubuntu repository targets
RUN sed -i -e 's|eoan|focal|g' /etc/apt/sources.list
RUN apt update --yes
RUN add-apt-repository ppa:deadsnakes/ppa

# install python3.9 and remove the symlink for python3.8
# and create a symlink for python3.9 instead
RUN apt install --yes python${PYTHON_VERSION}
RUN apt install --yes python3-pip
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python3


# Copy build-relevant files/folders
RUN mkdir /pokemon
ENV HOME=/pokemon
WORKDIR $HOME
COPY ./project $HOME/project

COPY ./.env.${TARGET_ENV} $HOME
COPY ./docker-entrypoint.sh $HOME

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
WORKDIR $HOME/project
RUN poetry install --no-interaction --no-ansi

WORKDIR $HOME
EXPOSE 8000
RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]