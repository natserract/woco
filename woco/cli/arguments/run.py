import argparse

from typing import Union
from woco.cli.arguments.default_arguments import add_data_param, add_config_param
from woco.shared import constants

def set_run_arguments(parser: argparse.ArgumentParser) -> None:
    """Arguments for running Woco directly using `woco run`."""
    add_data_param(parser)
    add_config_param(parser)
    add_type_argument(parser)

def add_type_argument(
    parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup]
) -> None:
    """Add an argument for type."""
    parser.add_argument(
        "-t",
        "--type",
        default=constants.DEFAULT_METHOD_TYPE,
        choices=['post', 'patch'],
        help="Type of request methods to send data to WordPress REST API",
    )
