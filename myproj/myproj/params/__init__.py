"""
Classes for dealing with project parameters.
"""
import collections.abc
import copy
from datetime import date
import logging
import os
import string
import sys
from typing import (Dict, List, Mapping)

logger = logging.getLogger(__name__)


class GetParams:
    """Gets any missing parameters for '.project.Project' from user."""
    def __init__(
        self,
        defaults: Mapping,
        params: Dict = {},
    ) -> None:
        """
        :param defaults: dictionary of suggested default values when asking
                the user to supply missing configuration parameters
                interactively; must conform to model in
                '.models.Defaults'
        :param params: dictionary of configuration values; must conform to
                model in '.models.Parameters'

        :returns: None
        """
        self.params = params
        self.defaults = defaults
        self.get_params()

    def get_params(self, retries: int = 5) -> None:
        """Get missing parameters from user.

        :param retries: use default value after user has entered n invalid
                inputs. Set to negative value to keep asking the user
                infinitely as long as the input remains invalid.

        :returns: None
        :raises: re-raises TypeError and KeyboardInterrupt from query_user()
        """
        # Organization params
        d = self.defaults['org']
        if "org" not in self.params:
            self.params['org'] = {}
        p = self.params['org']

        k = "name"
        if k not in p:
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "slug"
        if k not in p:
            d[k]['value'] = GetParams.slugify(s=p['name'])
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "copyright_owner"
        if k not in p:
            d[k]['value'] = p['name']
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "git_host"
        if k not in p:
            d[k]['value'] = "https://github.com/" + p['slug']
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "docker_host"
        if k not in p:
            d[k]['value'] = "registry.hub.docker.com/" + GetParams.slugify(
                s=p['name'],
                whitespace_replace="",
            )
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        # User params
        d = self.defaults['user']
        if "user" not in self.params:
            self.params['user'] = {}
        p = self.params['user']

        k = "name"
        if k not in p:
            try:
                d[k]['value'] = os.popen(
                    'git config --get user.name'
                ).read().rstrip()
            except Exception:
                pass
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "slug"
        if k not in p:
            d[k]['value'] = GetParams.slugify(s=p['name'])
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "email"
        if k not in p:
            try:
                d[k]['value'] = os.popen(
                    'git config --get user.email'
                ).read().rstrip()
            except Exception:
                d[k]['value'] = (
                    f"{p['slug']}@{self.params['org']['slug']}.com"
                )
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "affiliation"
        if k not in p:
            d[k]['value'] = self.params['org']['name']
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "url"
        if k not in p:
            d[k]['value'] = f"https://github.com/{p['slug']}"
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        # Project params
        d = self.defaults['project']
        if "project" not in self.params:
            self.params['project'] = {}
        p = self.params['project']

        k = "name"
        if k not in p:
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "slug"
        if k not in p:
            d[k]['value'] = GetParams.slugify(s=p['name'])
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "path"
        if k not in p:
            d[k]['value'] = f"{os.getcwd()}{os.sep}{p['slug']}"
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "synopsis"
        if k not in p:
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "version"
        if k not in p:
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "tags"
        if k not in p:
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "license"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "copyright_year"
        if k not in p:
            d[k]['value'] = date.today().year
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "original_author"
        if k not in p:
            d[k]['value'] = self.params['user']['name']
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "git_repo"
        if k not in p:
            d[k]['value'] = (
                f"{self.params['org']['git_host']}"
                f"{os.sep}{p['slug']}"
            )
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        k = "docker_image_name"
        if k not in p:
            d[k]['value'] = (
                f"{self.params['org']['docker_host']}"
                f"{os.sep}{p['slug']}"
            )
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries,
            )

        # Software & file params
        d = self.defaults['soft']
        if "soft" not in self.params:
            self.params['soft'] = {}
        p = self.params['soft']

        k = "python_version"
        if k not in p:
            d[k]['value'] = '.'.join([str(i) for i in sys.version_info[0:3]])
            p[k] = GetParams.query_user(
                d=d[k],
                retries=retries
            )

        k = "docs"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "docker"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "packaging"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "cli_script"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "linter"
        if k not in p:
            try:
                p[k] = GetParams.split_choices(s=GetParams.query_user(
                    d=d[k],
                    retries=retries,
                ))
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "testing"
        if k not in p:
            try:
                p[k] = GetParams.split_choices(s=GetParams.query_user(
                    d=d[k],
                    retries=retries,
                ))
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "ci_cd"
        if k not in p:
            try:
                p[k] = GetParams.split_choices(s=GetParams.query_user(
                    d=d[k],
                    retries=retries,
                ))
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

        k = "auto_version_bump"
        if k not in p:
            try:
                p[k] = GetParams.query_user(
                    d=d[k],
                    retries=retries,
                )
            except ValueError:
                logger.warning(
                    "Too many invalid inputs. Using default value "
                    f"'{d[k]['value']}'.")
                p[k] = d[k]['value']

    @staticmethod
    def query_user(
        d: Mapping,
        retries: int = -1,
    ) -> str:
        """Query user for parameters to be used for project setup.

        :param d: default dictionary of the minimal form {"value": "",
                "description": ""}.
        :param retries: how many times the user can retry entering input if it
                is invalid; a negative integer will allow indefinite inputs.

        :returns: str
        :raises: TypeError
        :raises: ValueError
        :raises: KeyboardInterrupt
        """
        if not isinstance(d, collections.abc.Mapping):
            raise TypeError(
                f"Type 'collections.abc.Mapping' expected, got '{type(d)}'"
            )
        if type(retries) is not int:
            raise TypeError(
                f"Type 'int' expected, got '{type(retries)}'"
            )
        try:
            # Build description
            choices = ""
            if "choices" in d:
                multi = ""
                alt = ""
                if d['multiple']:
                    multi = "or more "
                if d["alternative"]:
                    alt = f"; or pick '{d['alternative']}'"
                ls = ["'" + choice + "'" for choice in d['choices']]
                choices = (f"\n(pick one {multi}of {', '.join(ls)}{alt})")
            # Get user input, fall back to default
            s = input(
                "\n"
                f"{d['description']}\n"
                f"(default: '{d['value']}'){choices}\n"
                "> "
            )
            if not s:
                s = d["value"]
            # Validate user input
            if "choices" in d:
                allowed = d['choices']
                if d['alternative']:
                    allowed += [d['alternative']]
                if d['multiple']:
                    ls = [item.strip() for item in s.split(',')]
                    for item in ls:
                        if item not in allowed:
                            logger.warning(
                                f"\nIllegal value '{item}' entered. Please "
                                "try again."
                            )
                            if retries:
                                return GetParams.query_user(d=d, retries=retries - 1)
                            else:
                                raise ValueError(f"Too many wrong inputs.")
                else:
                    if s not in allowed:
                        logger.warning(
                            f"\nIllegal value '{s}' entered. Please try again."
                        )
                        if retries:
                            return GetParams.query_user(d=d, retries=retries - 1)
                        else:
                            raise ValueError(f"Too many wrong inputs.")
        except KeyError:
            raise TypeError(
                f"The provided defaults file is corrupt."
            )
        except KeyboardInterrupt:
            raise KeyboardInterrupt("\nProgram aborted by user.")
        return s

    @staticmethod
    def slugify(
        s: str,
        allowed_start: str = string.ascii_lowercase,
        allowed_end: str = string.ascii_lowercase + string.digits,
        allowed_rest: str = string.ascii_lowercase + string.digits + "_",
        lower: bool = True,
        whitespace_replace: str = "_",
    ) -> str:
        """Transforms string into 'machine-readable' slugs.

        :param s: string to be processed.
        :param allowed_start: string of characters allowed in the first
                position of the output string. The beginning of the input
                string will be trimmed until the first allowed character.
        :param allowed_end: string of characters allowed in the last
                position of the output string. The end of the input string
                will be trimmed from the last allowed character.
        :param allowed_rest: string of characters allowed in all but the first
                and last positions of the output string. Any characters that
                are not allowed will be removed from the input string.
        :param lower: whether uppercase characters should be transformed to
                lower case.
        :param whitespace_replace: string to replace all whitespace
                characters. Runs of whitespace characters will be replaced by
                a single instance of the string. Note that whitespace
                replacement occurs before checking of allowed characters takes
                place, so if this string contains characters not in the
                allowed characters, these characters will be removed.

        :returns: str
        :raises: TypeError
        """
        if not type(s) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(s)}'"
            )
        if not type(allowed_start) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(allowed_start)}'"
            )
        if not type(allowed_end) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(allowed_end)}'"
            )
        if not type(allowed_rest) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(allowed_rest)}'"
            )
        if not type(lower) is bool:
            raise TypeError(
                f"Type 'bool' expected, got '{type(lower)}'"
            )
        if not type(whitespace_replace) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(whitespace_replace)}'"
            )
        if lower:
            s = s.lower()
        s = whitespace_replace.join(s.split())
        c = 0
        for c in range(0, len(s)):
            if s[c] in allowed_start:
                break
        else:
            c += 1
        s = s[c:]
        d = len(s)
        for d in reversed(range(0, len(s))):
            if s[d] in allowed_end:
                break
        else:
            d -= 1
        s = s[:d+1]
        s = ''.join([c for c in s if c in allowed_rest])
        return s

    @staticmethod
    def split_choices(
        s: str,
        sep: List[str] = [','],
    ):
        """Splits a string into items based on a separator, then removes
        trailing whitespace from resulting items.

        Useful, for example, for splitting keywords/tags.

        :param s: input string.
        :param split: list of separator strings; all items will be used
                for splitting.

        :return: list of str
        :raises: TypeError
        """
        if not type(s) is str:
            raise TypeError(f"Type 'str' expected, got '{type(s)}'")
        if not type(sep) is list:
            raise TypeError(f"Type 'list' expected, got '{type(s)}'")
        for item in sep:
            if not type(item) is str:
                raise TypeError(f"Type 'str' expected, got '{type(s)}'")
        sep_cp = copy.copy(sep)
        current_sep = sep_cp.pop(0)
        split_string = [item.strip() for item in s.split(current_sep)]
        if sep_cp:
            split_further = []
            for item in split_string:
                split_further += GetParams.split_choices(item, sep=sep_cp)
            split_string = split_further
        return split_string
