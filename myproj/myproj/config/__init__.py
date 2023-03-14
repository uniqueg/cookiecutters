"""Config parser class and associated utils."""

__version__ = "0.1.0"
__copyright__ = "Copyright 2020 Zavolan lab, Biozentrum, University of Basel"
__license__ = "Apache License 2.0"
__author__ = "Alex Kanitz"
__maintainer__ = "Alex Kanitz"
__email__ = "alexander.kanitz@alumni.ethz.ch"

import collections.abc
import logging
from typing import (Any, Dict, Iterable, Mapping, Optional)

import addict
import yaml

logger = logging.getLogger(__name__)


class ConfigParser:
    """Parses one or more nested YAML configuration files.

    Conflicing field values are overridden in the order in which files are
    specified.
    """

    def __init__(
        self,
        *config_files: Optional[Iterable[str]],
        log: bool = False,
        **log_kwargs,
    ) -> None:
        """Class constructor.

        Configuration values are available as a dictionary in property
        `values`.

        :param *config_files: iterable of paths to YAML configuration files.
        "param **log_kwargs: passed to the logging function `log_yaml()`;
                ignored if `log` is `False`.
        """
        self.values: Dict = {}
        if config_files:
            self.values = self.read_config_files(*config_files)
        if log:
            if self.values:
                self.log_yaml(**self.values, **log_kwargs)
            else:
                self.log_yaml(
                    **{"Dictionary empty": "no parameters found"},
                    **log_kwargs,
                )

    @staticmethod
    def read_config_files(*config_files) -> Dict:
        """Read one or more nested configuration YAML files.

        :param *config_files: iterable of paths to YAML configuration files.

        :returns: dict
        """
        params = {}
        for conf in config_files:
            contents = ConfigParser.yaml_to_dict(yaml_file=conf)
            params = ConfigParser.recursive_dict_update(
                original=params,
                update=contents,
            )

        return params

    @staticmethod
    def yaml_to_dict(yaml_file: str) -> Dict:
        """Returns contents of YAML file as dictionary.

        :param file: YAML file.
        :param safe: whether to use the safe loader or not.

        :returns: Dict
        :raises: TypeError (if not dict or None is produced)
        :raises: FileNotFoundError
        :raises: yaml.parser.ParserError
        """
        yaml_dict = {}
        try:
            with open(yaml_file, 'r') as fh:
                yaml_dict = yaml.safe_load(fh)
                if yaml_dict is None:
                    yaml_dict = {}
                elif type(yaml_dict) is not dict:
                    raise TypeError(
                        f"File `{yaml_file}` cannot be converted to "
                        "dictionary"
                    )
        except FileNotFoundError:
            logger.exception(f"YAML file '{yaml_file}' not available")
            raise
        except Exception:
            logger.exception(
                (
                    f"YAML file '{yaml_file}' could not be opened or "
                    "parsed"
                )
            )
            raise

        return yaml_dict

    @staticmethod
    def dict_to_yaml(d: Mapping, yaml_file: str) -> None:
        """Writes dictionary to YAML file.

        :param d: dictionary to convert to YAML file.
        :param file: desired file path for YAML output file; it will be
                attempted to overwrite any existing file at this path.

        :returns: None
        :raises: TypeError
        :raises: FileNotFoundError
        :raises: yaml.representer.RepresenterError
        """
        if not isinstance(d, collections.abc.Mapping):
            raise TypeError(
                f"Type 'collections.abc.Mapping' expected, got '{type(d)}'"
            )
        if not type(yaml_file) is str:
            raise TypeError(
                f"Type 'str' expected, got '{type(yaml_file)}'"
            )
        try:
            with open(yaml_file, 'w') as fh:
                yaml.safe_dump(
                    data=d,
                    stream=fh,
                )
        except yaml.representer.RepresenterError:
            logger.exception("Object could not be represented as YAML.")
            raise
        except Exception:
            logger.warning(
                f"Configuration file '{yaml_file}' could not produced."
            )

        return None

    @staticmethod
    def log_yaml(
        header: Optional[str] = None,
        level: int = logging.DEBUG,
        logger: logging.Logger = logging.getLogger(__name__),
        **kwargs,
    ) -> None:
        """Logs each of a number of keyword arguments with the indicated
        logging level in YAML format.

        Dictionaries and iterable objects are logged recursively.

        :param header: if not `None`, the header is logged before any of the
                keyword arguments are processed.
        :param level: logging level.
        :param logger: the logger to be used.

        :returns: None
        """
        try:
            # Log header
            if header is not None:
                logger.log(level, header)

            # Log value
            if kwargs:
                text = yaml.safe_dump(
                    kwargs,
                    allow_unicode=True,
                    default_flow_style=False
                ).splitlines()
                for line in text:
                    logger.log(level, line)
        except Exception as e:
            logger.log(level, f"Error occurred during logging: {e}")

    @staticmethod
    def recursive_dict_update(original: Mapping, update: Mapping):
        """Recursively updates a dictionary.

        :param original: dictionary used as baseline for the update.
        :param update: dictionary used to update original dictionary values.

        :returns: dict
        :raises: TypeError
        """
        if not isinstance(original, collections.abc.Mapping):
            raise TypeError(
                "Argument 'original' requires type 'collections.abc.Mapping'"
                f"but got '{type(original)}'"
            )
        if not isinstance(update, collections.abc.Mapping):
            raise TypeError(
                "Argument 'update' requires type 'collections.abc.Mapping'"
                f"but got '{type(update)}'"
            )
        d = addict.Dict(original)
        d.update(update)
        return d.to_dict()

    @staticmethod
    def same_keys(
        query: Any,
        ref: Mapping,
        two_way: bool = False
    ) -> bool:
        """Checks whether a query dictionary has all of the keys that a
        reference dictionary has.

        Nesting of dictionaries is supported.

        :param query: query object
        :param ref: reference dictionary
        :param two_way: whether the inverse comparison should be done as well,
            so 'True' is only returned if all keys (and thus the dictionary
            structure) are identical

        :returns: bool
        :raises: TypeError
        """
        if not isinstance(ref, collections.abc.Mapping):
            raise TypeError(
                "Argument 'ref' requires type 'collections.abc.Mapping' but "
                f"'{type(ref)}'"
            )
        for k, v in ref.items():
            try:
                if k in query:
                    if isinstance(v, collections.abc.Mapping) and v:
                        if not ConfigParser.same_keys(
                            query=query[k],
                            ref=v,
                            two_way=False
                        ):
                            return False
                else:
                    return False
            except Exception:
                return False
        if two_way:
            if not ConfigParser.same_keys(
                query=ref,
                ref=query,
                two_way=False
            ):
                return False
        return True
