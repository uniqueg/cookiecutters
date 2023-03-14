#!/usr/bin/env python

"""{{cookiecutter.project_description}}
"""

__version__ = "{{cookiecutter.project_version}}"
__copyright__ = "Copyright {{cookiecutter.copyright_year}} {{cookiecutter.copyright_owner}}"
__license__ = "{{cookiecutter.project_license}}"
__author__ = "{{cookiecutter.author_name}}"
__maintainer__ = "{{cookiecutter.author_name}}"
__email__ = "{{cookiecutter.author_email}}"

# TODO AUTHOR: add here built-in modules
import argparse
import logging
import sys

# TODO AUTHOR: add here third party modules

# TODO AUTHOR: add here own modules

logger = logging.getLogger(__name__)


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        # TODO AUTHOR: add here detailed tool description; leave a blank line
        # in between synopsis and extended description
        description=sys.modules[__name__].__doc__,
    )

    # TODO AUTHOR: add here optional and positional arguments as per argparse
    # docs; for many optional arguments, consider adding argument groups for
    # clarity
    parser.add_argument(
        '--verbose', "-v",
        action='store_true',
        default=False,
        help="print logging messages to STDERR",
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help="also print debugging messages to STDERR",
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
        help="show version information and exit",
    )

    return parser.parse_args()


def setup_logging(
    logger: logging.Logger,
    verbose: bool = False,
    debug: bool = False,
):
    """Configure logging."""
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


def main():
    args = parse_args()
    setup_logging(
        logger=logger,
        verbose=args.verbose,
        debug=args.debug,
    )
    # TODO AUTHOR: Put main code here. Options and positional arguments are in
    # `args`, logging can be used with `logger`; see (and delete) example log
    # message below
    logger.info(f"Started script. Option `--verbose` set? {args.verbose}")


if __name__ == "__main__":
    main()
