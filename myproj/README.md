# Cookiecutter template for Python CLI tool

Set up project directory with required files, including `README.md`, license,
`.gitignore`, `Dockerfile` and GitLab CI config.

## Usage

Install `cookiecutter`:

```sh
pip install cookiecutter
```

Clone repository:

```sh
git clone ssh://git@git.scicore.unibas.ch:2222/zavolan_group/admin/templates/cookiecutter-cli_script_py.git
```

Create project:

```sh
cookiecutter cookiecutter-cli_script_py
```

Enter desired values (simply press `<ENTER>` to keep defaults). A directory
with the name of the `project_slug` parameter will be created in the current
working directory.
