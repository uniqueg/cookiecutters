## Set base image
FROM python:{{cookiecutter.soft.python_version}}

## Set metadata
LABEL base.image="python:{{cookiecutter.soft.python_version}}"
LABEL software="{{cookiecutter.project.slug}}"
LABEL software.version="{{cookiecutter.project.version}}"
LABEL software.description="{{cookiecutter.project.synopsis}}"
LABEL software.website="{{cookiecutter.project.git_repo}}"
LABEL software.documentation="{{cookiecutter.project.git_repo}}"
LABEL software.license="{{cookiecutter.project.license"
LABEL software.tags="{{cookiecutter.project.tags}}"
LABEL maintainer="{{cookiecutter.user.name}}"
LABEL maintainer.email="{{cookiecutter.user.email}}"
LABEL maintainer.organisation="{{cookiecutter.org.name}}"

## Set variables
ARG USER="user"
ARG GROUP="usergroup"
ARG WORKDIR="/home/${USER}/{{cookiecutter.project.slug}}/"
ENV PATH="${WORKDIR}:${PATH}"

## Create and set working directory
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

## Copy and install required packages
COPY ./requirements.txt ${WORKDIR}
RUN pip install -r requirements.txt

## Copy remaining files
COPY src/ ${WORKDIR}/src
COPY tests/ ${WORKDIR}/tests
COPY LICENSE README.md ${WORKDIR}

## Set up environment
RUN groupadd -r ${GROUP} && \
    useradd --no-log-init -r -g ${GROUP} ${USER} && \
    chown -R ${USER}:${GROUP} ${WORKDIR} && \
    chmod 700 ${WORKDIR}
USER ${USER}
{{cookiecutter.replace.soft.docker_entrypoint}}
ENTRYPOINT ["src/{{cookiecutter.project.slug}}.py"]
