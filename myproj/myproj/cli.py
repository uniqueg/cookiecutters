#!/usr/bin/env python
"""
Initialize Python project.
"""

# TODO:
# - save user config
# - prepare project template
# - render project template
# - clean up
# - logging issue
# - import issue
# - ? remove defaults.yaml, get from model
# - add conda
# - add virtual environment

__version__ = "0.1.0"
__copyright__ = "Copyright 2020 Zavolan lab, Biozentrum, University of Basel"
__license__ = "Apache License 2.0"
__author__ = "Alex Kanitz"
__maintainer__ = "Alex Kanitz"
__email__ = "alexander.kanitz@alumni.ethz.ch"

import argparse
import logging
import os
import sys
from typing import (Optional, Sequence)

from myproj.config import ConfigParser
from myproj.models import Defaults
from myproj.params import GetParams
from myproj.project import Project

logger = logging.getLogger()


def parse_cli_args(args: Optional[Sequence[str]]) -> argparse.Namespace:
    """Parse CLI arguments.

    :param args: iterable containing command line parameters and arguments.

    :returns: argparse.Namespace
    :raises: re-raises any 'argparse' Exceptions
    """
    parser = argparse.ArgumentParser(
        description=str(sys.modules[__name__].__doc__) + """

        The first time the program is run, the user is queried for project-
        and user-specific (author name and contact information,
        organization/affiliation, preferences, etc.) parameters to be used to
        set up the project. User-specific parameters are then saved in a
        dedicated configuration file which is read on every subsequent run of
        the program in order to minimize user interaction. This behavior can
        be modified by the available options."""
    )

    parser.add_argument(
        '--defaults',
        type=argparse.FileType('r', encoding='UTF-8'),
        default=os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "config",
            "defaults.yaml",
        ),
        help=(
            "Can be used to supply a different default values file than the "
            "one that is shipped with this package and which is used by "
            "default. If specified, the path should lead to a file that "
            "corresponds precisely to the original defaults file. Use with "
            "care."
        ),
        metavar="PATH",
    )

    config = parser.add_mutually_exclusive_group()
    config.add_argument(
        '--config',
        type=argparse.FileType('r', encoding='UTF-8'),
        action="append",
        default=[os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "config",
            "user_config.yaml",
        )],
        help=(
            "Use the provided YAML configuration file instead of the default "
            "user-specific configuration. This option can be used to "
            "completely forego user interaction. Howerver, this requires "
            "that the specified configuration file defines values for all "
            "parameters in the defaults file available at path "
            "'config/defaults.yaml' relative to the root of the project "
            "repository. Parameters that are not required by the program are "
            "silently ignored. Note that the option can be provided multiple "
            "times. In that case, the specified configuration files are "
            "parsed in the provided order, with conflicting values "
            "overriding any previously set ones. This can be used to "
            "override specific values of the default user-specific parameter "
            "file (located at 'config/user_config.yaml' relative to project "
            "root) or to provide a file with only only project-specific "
            "parameters to ensure that the execution in non-interactive."
        ),
        metavar="PATH",
    )
    config.add_argument(
        '--no-config',
        dest="config",
        action='store_const',
        const=None,
        help=(
            "Query user for all parameters; do not read user-specific "
            "paramaters from configuration file."
        )
    )

    parser.add_argument(
        '--verbose', "-v",
        action='store_true',
        default=False,
        help="Print logging messages to STDERR.",
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help="Print debugging messages to STDERR. Implies `--verbose`.",
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
        help="Show version information and exit.",
    )

    args_parsed = parser.parse_args(args)

    if args_parsed.defaults:
        args_parsed.defaults.close()
        args_parsed.defaults = args_parsed.defaults.name

    if args_parsed.config:
        conf_list = []
        for conf in args_parsed.config:
            if not isinstance(conf, str):
                conf.close()
                conf_list.append(conf.name)
            else:
                conf_list.append(conf)

        args_parsed.config = conf_list

    return args_parsed


def setup_logging(
    logger: Optional[logging.Logger] = None,
    verbose: bool = False,
    debug: bool = False,
) -> None:
    """Configure logging.

    :param logger: logging object to use for logging.
    :param verbose: whether info messages should be logged.
    :param debug: whether debug messages should be logged.

    :returns: None
    """
    if logger:
        if debug:
            logger.setLevel(logging.DEBUG)
        elif verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "[%(asctime)-15s: %(levelname)-8s @ %(funcName)s] %(message)s"
        ))
        logger.addHandler(handler)


def main(
    defaults_file: str = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "config",
        "defaults.yaml",
    ),
    config_files: Optional[Sequence[str]] = [os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "config",
        "user_config.yaml",
    )],
) -> None:
    """Main function for Python project creation.

    :param defaults_file: YAML file containing default values for user and
            project parameters; needs to conform to '.models.Defaults'.
    :param config_files: ordered list of YAML files containing actual values
            user and project parameters, parsed and overridden in the listed
            order; users will only be queried for any required parameter
            values missing here.

    :returns: None
    """
    try:

        # Parse defaults
        logger.debug(f"Reading defaults file '{defaults_file}'...")
        defaults = ConfigParser(
            defaults_file,
            log=True,
            header="=== PARAMETER DEFAULT VALUES ===",
        )

        # Validate defaults
        if not ConfigParser.same_keys(
            query=defaults.values,
            ref=Defaults().to_dict()
        ):
            raise TypeError(
                f"The provided defaults file '{defaults_file}' is corrupt."
            )

        # Parse config
        if not config_files:
            logger.debug(
                "Config parsing skipped because option '--no-config' supplied."
            )
            params = ConfigParser(
                log=True,
                header="=== USER-DEFINED PARAMETER VALUES ===",
            )
        else:
            logger.debug(f"Reading config files {config_files}...")
            params = ConfigParser(
                *config_files,
                log=True,
                header="=== LOADED CONFIG PARAMETERS ===",
            )

        # Get missing parameters
        params = GetParams(
            defaults=defaults.values,
            params=params.values,
        )
        logger.debug(f"Reading config files {config_files}...")
        ConfigParser.log_yaml(
            header="=== COMPLETE CONFIG PARAMETERS ===",
            **params.params,
        )

        # Save parameters in user config
        user_config = {
            'org': params.params['org'],
            'user': params.params['user'],
            'soft': params.params['soft'],
        }
        user_config_file = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "config",
            "user_config.yaml",
        )
        ConfigParser.dict_to_yaml(
            d=user_config,
            yaml_file=user_config_file,
        )

        # Set up project
        project = Project(params.params)
        try:
            project.prepare_template()
        except Exception:
            logger.error(
                "An error occured during the creation of the project "
                f"template. The template directory '{project.temp_dir}' "
                "will be removed."
            )
            try:
                # project.clean_up()
                logger.warning("Re-activate cleanup and remove this warning.")
            except Exception:
                logger.error(
                    "An error occured during cleanup of the project. Please "
                    "manually remove the template directory."
                )
                raise
            raise

        # Render project
        try:
            project.render_project()
        except FileExistsError:
            try:
                logger.error(
                    "An error occured during the creation of the project "
                    f"template. The template directory '{project.temp_dir}' "
                    "will be removed."
                )
                # project.clean_up()
                logger.warning("Re-activate cleanup and remove this warning.")
            except Exception:
                logger.error(
                    "An error occured during cleanup of the project. Please "
                    "manually remove the template and project directories."
                )
                raise
            raise
        except Exception:
            logger.error(
                "An error occured during rendering of the project. "
                f"The template directory '{project.temp_dir}' and the "
                f"project directory '{project.project_dir} will be "
                "removed."
            )
            try:
                # project.clean_up(include_project_dir=True)
                logger.warning("Re-activate cleanup and remove this warning.")
            except Exception:
                logger.error(
                    "An error occured during cleanup of the project. Please "
                    "manually remove the template and project directories."
                )
                raise
            raise

        # Clean up
        try:
            # project.clean_up()
            logger.warning("Re-activate cleanup and remove this warning.")
        except Exception:
            logger.error(
                "An error occured during cleanup of the project. Please "
                "manually remove the template and project directories."
            )
            raise

    except Exception:
        logger.exception("Program finished with non-zero exit status.")
        sys.exit(1)
    else:
        logger.info("Program finished.")
        sys.exit(0)


if __name__ == "__main__":
    args = parse_cli_args(sys.argv[1:])
    setup_logging(
        logger=logger,
        verbose=args.verbose,
        debug=args.debug,
    )
    logger.info("Program started.")
    main(
        defaults_file=args.defaults,
        config_files=args.config,
    )
