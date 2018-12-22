# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=kivymd-linux --file=dockerfiles/Dockerfile-linux .
# Run with:
# docker run kivymd-linux /bin/sh -c 'tox'
# Or using the entry point shortcut:
# docker run kivymd-linux 'tox'
# Or for interactive shell:
# docker run -it --rm kivymd-linux
FROM ubuntu:18.04

# configure locale
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install system dependencies
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
	python3 virtualenv tox

WORKDIR /app
COPY . /app
ENTRYPOINT ["./dockerfiles/start.sh"]
