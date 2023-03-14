"""
Classes for project templating and rendering.
"""
import json
import logging
import os
import pathlib
import shutil
import tempfile
from typing import Dict

from myproj.config import ConfigParser
from myproj.models import (
    CI_CD, License, Linter, Parameters, TestSuite, YesNo
)

logger = logging.getLogger(__name__)


class Project:
    """Generate Python package.

    Sets up and renders a project-specific, temporary Cookiecutter template
    for the creation of a boilerplate Python project with support for licenses,
    docs, packaging, containerization, publishing options and CI/CD.
    """

    def __init__(
        self,
        params: Dict,
        replacement_yaml: str = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'config',
            'replacement_strings.yaml',
        )
    ) -> None:
        """Initialize Project instance with required parameters.

        :param params: dictionary of required project parameters.
        :param replacement_yaml: YAML file with values for context-dependent
                string replacements.

        :returns: None
        :raises: TypeError
        """
        self.params = params
        self.replacement_yaml = replacement_yaml
        if not ConfigParser.same_keys(
            query=self.params,
            ref=Parameters().to_dict(),
            two_way=True,
        ):
            raise TypeError(
                "Not all required parameters were provided."
            )
        self.project_dir = self.params['project']['path']

    def prepare_template(
        self,
        root_dir: str = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            "tmp"
        ),
    ) -> None:
        """Set up temporary custom Cookiecutter with templates and default
        values according to project parameters.

        :param root_dir: root directory for creating temporary Cookiecutter
                project directories.

        :returns: None
        :raises: IOError
        :raises: KeyError
        """
        # Create template directory
        try:
            pathlib.Path(root_dir).mkdir(parents=True, exist_ok=True)
            self.temp_dir = tempfile.mkdtemp(dir=root_dir)
        except Exception:
            raise IOError("Could not create temporary project directory.")
        logger.info(
            f"Created project template directory at '{self.temp_dir}'."
        )

        # Create destination directory
        dst_dir = os.path.join(
            self.temp_dir,
            '{{cookiecutter.project.slug}}'
        )
        try:
            pathlib.Path(dst_dir).mkdir(parents=False, exist_ok=False)
        except Exception:
            raise IOError("Could not create template directory.")

        # Set source directory
        src_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'templates',
        )

        # Get text replacement strings
        self.params['replace'] = ConfigParser.yaml_to_dict(
            yaml_file=self.replacement_yaml,
        )
        ConfigParser.log_yaml(
            header="=== REPLACEMENT STRING VALUES ===",
            **self.params['replace'],
        )
        rep = self.params['replace']

        # Initialize requirements
        requirements = []

        # Copy '.gitignore' file
        file_src = os.path.join(src_dir, 'version_control', '.gitignore')
        shutil.copy2(src=file_src, dst=dst_dir)

        # Copy license
        if self.params['project']['license'] != 'none':
            file_src = os.path.join(
                src_dir,
                'licenses',
                License[self.params['project']['license']].value
            )
            file_dst = os.path.join(dst_dir, 'LICENSE')
            shutil.copy2(src=file_src, dst=file_dst)

        # Copy 'contributors.md' file
        file_src = os.path.join(src_dir, 'contributing', 'contributors.md')
        shutil.copy2(src=file_src, dst=dst_dir)

        # Copy packaging files
        if YesNo[self.params['soft']['packaging']].value:
            file_src = os.path.join(src_dir, 'packaging', 'setup.py')
            shutil.copy2(src=file_src, dst=dst_dir)
            file_src = os.path.join(src_dir, 'packaging', 'MANIFEST.in')
            shutil.copy2(src=file_src, dst=dst_dir)
            requirements.extend(['setuptools_git', 'twine'])

        # Copy `Dockerfile`
        if YesNo[self.params['soft']['docker']].value:
            file_src = os.path.join(src_dir, 'containers', 'Dockerfile')
            shutil.copy2(src=file_src, dst=dst_dir)

        # Add linters
        if 'none' not in self.params['soft']['linter']:
            requirements.extend(
                [Linter[item].value for item in self.params['soft']['linter']]
            )

        # Add test suites
        if 'none' not in self.params['soft']['testing']:
            requirements.extend(
                [TestSuite[item].value for item in \
                    self.params['soft']['testing']]
            )

        # Copy CI/CD configs
        if 'none' not in self.params['soft']['ci_cd']:
            for item in self.params['soft']['ci_cd']:
                file_src = os.path.join(
                    src_dir,
                    'ci_cd',
                    CI_CD[item].value,
                )
                shutil.copy2(src=file_src, dst=dst_dir)
            if not requirements:
                rep['ci_cd']['install_requirements']['gitlab_docker'] = ""
            if 'pytest' not in self.params['soft']['testing']:
                rep['ci_cd']['test_pytest']['gitlab_docker'] = ""
            if 'flake8' not in self.params['soft']['linter']:
                rep['ci_cd']['test_flake8']['gitlab_docker'] = ""
            if self.params['soft']['cli_script'] == "no":
                rep['ci_cd']['test_cli']['gitlab_docker'] = ""

        logger.warning(requirements)

        # Write requirements to file
        requirements_file = os.path.join(
            dst_dir,
            'requirements.txt',
        )
        with open(requirements_file, 'w') as fh:
            fh.write('\n'.join(requirements))

        # Write cookiecutter config JSON to file
        cookiecutter_config_file = os.path.join(
            self.temp_dir,
            'cookiecutter.json',
        )
        params_json = json.dumps(self.params, indent=2)
        with open(cookiecutter_config_file, 'w') as fh:
            fh.write(params_json)

    def render_project(
        self,
    ) -> None:
        """Render project template with user-defined parameters.

        :returns: None
        """
        try:
            pathlib.Path(self.project_dir).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            logger.error(
                "Desired project directory already exists. For safety "
                "reasons, no changes were made. Please specify a "
                "non-existing directory for the project path."
            )
            raise

    def clean_up(
        self,
        include_project_dir: bool = False,
    ) -> None:
        """Removes project template directory and other artefacts.

        :param include_project_dir: whether to include rendered project
                directory.

        :returns: None
        :raises: AttributeError
        :raises: FileNotFoundError
        :raises: NotADirectoryError
        :raises: PermissionsError
        """
        try:
            logger.debug(
                f"Removing temporary directory '{self.temp_dir}'."
            )
            shutil.rmtree(self.temp_dir)
        except AttributeError:
            logger.error(
                "Temporary project directory is unset and could not be "
                "removed."
            )
            raise
        except (
            PermissionError,
            FileNotFoundError,
            NotADirectoryError
        ):
            logger.error(
                f"Project directory '{self.temp_dir}' could not be removed."
            )
            raise
        if include_project_dir:
            try:
                logger.debug(
                    f"Removing project directory '{self.project_dir}'."
                )
                shutil.rmtree(self.project_dir)
            except AttributeError:
                logger.error(
                    "Project directory is unset and could not be removed."
                )
                raise
            except (
                PermissionError,
                FileNotFoundError,
                NotADirectoryError
            ):
                logger.error(
                    f"Project directory '{self.project_dir}' could not be "
                    "removed."
                )
                raise
