"""
Model classes for representing nested data structures.
"""
import enum
from typing import Dict


class License(enum.Enum):
    """Enumerator class for supported software licenses."""
    apache2 = "apache2"
    gplv3 = "gplv3"
    mit = "mit"
    mozilla2 = "mozilla2"


class YesNo(enum.Enum):
    """Enumerator class for yes-no questions."""
    no = False
    yes = True


class Linter(enum.Enum):
    """Enumerator class for supported linters."""
    black = "black"
    flake8 = "flake8"
    pylint = "pylint"
    pyright = "pyright"


class TestSuite(enum.Enum):
    """Enumerator class for supported test suites."""
    pytest = "pytest"


class CI_CD(enum.Enum):
    """Enumerator class for supported CI/CD engines."""
    gitlab_docker = ".gitlab-ci.yml"


class Parameters:
    """Collection of required fields for project config file or object."""
    def __init__(self) -> None:
        # Organization parameters
        self.org: dict = dict()
        self.org['name'] = ""
        self.org['slug'] = ""
        self.org['copyright_owner'] = ""
        self.org['git_host'] = ""
        self.org['docker_host'] = ""
        # User parameters
        self.user: dict = dict()
        self.user['name'] = ""
        self.user['slug'] = ""
        self.user['email'] = ""
        self.user['affiliation'] = ""
        self.user['url'] = ""
        # Project parameters
        self.project: dict = dict()
        self.project['name'] = ""
        self.project['slug'] = ""
        self.project['path'] = ""
        self.project['synopsis'] = ""
        self.project['version'] = ""
        self.project['tags'] = ""
        self.project['license'] = ""
        self.project['copyright_year'] = ""
        self.project['original_author'] = ""
        self.project['git_repo'] = ""
        self.project['docker_image_name'] = ""
        # Files and software parameters
        self.soft: dict = dict()
        self.soft['python_version'] = ""
        self.soft['docs'] = ""
        self.soft['docker'] = ""
        self.soft['packaging'] = ""
        self.soft['cli_script'] = ""
        self.soft['linter'] = ""
        self.soft['testing'] = ""
        self.soft['ci_cd'] = ""
        self.soft['auto_version_bump'] = ""

    def to_dict(self) -> Dict:
        """Return instance attributes as dictionary."""
        _excluded_keys = set(Parameters.__dict__.keys())
        return dict(
            (key, value) for (key, value) in self.__dict__.items()
            if key not in _excluded_keys
        )


class Defaults(Parameters):
    """Collection of required fields for project defaults file or object."""
    def __init__(self) -> None:
        Parameters.__init__(self)
        regular_dict = {
            "value": "",
            "description": "",
        }
        choice_dict = {
            "value": "",
            "choices": [],
            "multiple": False,
            "alternative": "",
            "description": "",
        }
        # Organization parameters
        self.org['name'] = regular_dict
        self.org['slug'] = regular_dict
        self.org['copyright_owner'] = regular_dict
        self.org['git_host'] = regular_dict
        self.org['docker_host'] = regular_dict
        # User parameters
        self.user['name'] = regular_dict
        self.user['slug'] = regular_dict
        self.user['email'] = regular_dict
        self.user['affiliation'] = regular_dict
        self.user['url'] = regular_dict
        # Project parameters
        self.project['name'] = regular_dict
        self.project['slug'] = regular_dict
        self.project['path'] = regular_dict
        self.project['synopsis'] = regular_dict
        self.project['version'] = regular_dict
        self.project['tags'] = regular_dict
        self.project['license'] = choice_dict
        self.project['copyright_year'] = regular_dict
        self.project['original_author'] = regular_dict
        self.project['git_repo'] = regular_dict
        self.project['docker_image_name'] = regular_dict
        # Files and software parameters
        self.soft['python_version'] = regular_dict
        self.soft['docs'] = choice_dict
        self.soft['docker'] = choice_dict
        self.soft['packaging'] = choice_dict
        self.soft['cli_script'] = choice_dict
        self.soft['linter'] = choice_dict
        self.soft['testing'] = choice_dict
        self.soft['ci_cd'] = choice_dict
        self.soft['auto_version_bump'] = choice_dict
