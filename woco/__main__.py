import json
import os
import argparse
import sys
import logging
import logging.config
import platform

from typing import List
from woco import version
from woco.cli import run
from woco.cli.arguments.default_arguments import add_logging_options
from woco.shared.utils import configure_logging

logger = logging.getLogger(__name__)

def create_argument_parser() -> argparse.ArgumentParser:
    """Parse all the command line arguments for the training script."""
    parser = argparse.ArgumentParser(
        prog="woco",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Woco command line interface.",
    )

    parser.add_argument(
        '--version',
        action='store_true',
        default=argparse.SUPPRESS,
        help="Print installed Woco version",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    add_logging_options(parent_parser)
    parent_parsers = [parent_parser]
    subparsers = parser.add_subparsers(help="Woco commands")

    run.add_subparser(subparsers, parents=parent_parsers)
    return parser

def print_version() -> None:
    """Prints version information of woco tooling and python."""
    print(f"Woco Version      :         {version.__version__}")
    print(f"Python Version    :         {platform.python_version()}")
    print(f"Operating System  :         {platform.platform()}")
    print(f"Python Path       :         {sys.executable}")

def main() -> None:
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    log_level = getattr(cmdline_arguments, "loglevel", None)
    configure_logging(log_level)

    try:
        if hasattr(cmdline_arguments, "func"):
            cmdline_arguments.func(cmdline_arguments)
        elif hasattr(cmdline_arguments, "version"):
            print_version()
        else:
            # user has not provided a subcommand, let's print the help
            logger.error("No command specified.")
            arg_parser.print_help()
            sys.exit(1)
    except Exception as e:
            # these are exceptions we expect to happen (e.g. invalid training data format)
            # it doesn't make sense to print a stacktrace for these if we are not in
            # debug mode
            logger.debug("Failed to run CLI command due to an exception.", exc_info=e)
            print(f"{e.__class__.__name__}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
