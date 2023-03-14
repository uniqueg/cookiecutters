## Set base image
FROM python:{{cookiecutter.python_version}}

## Set metadata
LABEL base.image="python:{{cookiecutter.python_version}}"
LABEL version="{{cookiecutter.project_version}}"
LABEL software="{{cookiecutter.project_slug}}"
LABEL software.version="{{cookiecutter.project_version}}"
LABEL software.description="{{cookiecutter.project_description}}"
LABEL software.website="{{cookiecutter.project_git_repo}}"
LABEL software.documentation="{{cookiecutter.project_git_repo}}/blob/master/README.md"
LABEL software.license="{{cookiecutter.project_git_repo}}/blob/master/LICENSE"
LABEL software.tags="{{cookiecutter.project_tags}}"
LABEL maintainer="{{cookiecutter.author_name}}"
LABEL maintainer.email="{{cookiecutter.author_email}}"
LABEL maintainer.organisation="{{cookiecutter.author_affiliation}}"

## Set variables
ARG USER="user"
ARG GROUP="usergroup"
ARG WORKDIR="/home/${USER}/{{cookiecutter.project_slug}}/"
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
ENTRYPOINT ["src/{{cookiecutter.project_slug}}.py"]