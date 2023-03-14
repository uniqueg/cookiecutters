# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Usage

> **AUTHOR:** Add usage string; take from output of help screen

```sh
python {{cookiecutter.project_slug}}.py [-hv] # replace with final usage string
```

## Parameters

> **AUTHOR:** Put here description of all required parameters and options; take
> from output of help screen

```console
```

## File formats

> **AUTHOR:** Add here descriptions to used file formats (required and
> optional):
>
> - links to specifications (if available) or detailed descriptions
> - detailed descriptions or specifications of any custom file formats,
>   including an example
>  
> Ideally also add these info to the help screen of the script itself!

## Extended usage

> **AUTHOR:** Example commands to run the tool with small test files added to
> the `/tests` directory (and included in the repository) should be added below
> (dockerized and non-dockerized) allow users to verify that the tool works.
> This integration test should also be included in the test suite and CI
> configuration.

### Run locally

In order to use the script, you will need to clone the repository and install
the dependencies:

```sh
git clone {{cookiecutter.project_git_repo}}
cd {{cookiecutter.project_slug}}
pip install requirements.txt
# Optional: run tests
pytest
```

> **NOTE:** You may want to install dependencies inside a virtual environment,
> e.g., using [`virtualenv`](https://virtualenv.pypa.io/en/latest/).

You can then find the script in directory `src/` and run it as described in
the [Usage](#Usage) section.

### Run inside container

If you have [Docker](https://www.docker.com/) installed, you can also pull the
Docker image:

```sh
docker pull {{cookiecutter.project_docker_repo}}
```

The script can be found in directory `/home/user/{{cookiecutter.project_slug}}/src` inside the
Docker container.

> **NOTE:** To run the tool on your own data in that manner, you will probably
> need to [mount a volume](https://docs.docker.com/storage/volumes/) to allow
> the container read input files and write persistent output from/to the host
> file system.

### Run test suite

Inside the root directory of the repository, run `pytest` to run a suite of
unit/integration tests.

## Tags

{{cookiecutter.project_tags}}

## Version

{{cookiecutter.project_version}}

## Contact

- Maintainer:
  [{{cookiecutter.author_name}}]({{cookiecutter.author_gitlab_profile}})
- Affiliation: {{cookiecutter.author_affiliation}}
- Email: {{cookiecutter.author_email}}
