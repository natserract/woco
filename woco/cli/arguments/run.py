import argparse

from typing import Union
from woco.cli.arguments.default_arguments import add_data_param, add_config_param, add_key_param
from woco.shared import constants

def set_run_arguments(parser: argparse.ArgumentParser) -> None:
    """Arguments for running Woco directly using `woco run`."""
    add_data_param(parser)
    add_config_param(parser)
    add_disable_out_files(parser)
    add_media_source(parser)

def set_run_update_arguments(parser: argparse.ArgumentParser) -> None:
    add_config_param(parser)
    add_media_source(parser)
    add_key_param(parser)

def set_run_remove_arguments(parser: argparse.ArgumentParser) -> None:
    add_config_param(parser)
    add_media_source(parser)
    add_key_param(parser)

def add_disable_out_files(
    parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup]
) -> None:
    """Add an argument for disable out files (.woco) """
    parser.add_argument(
        "--disable-out-file",
        default=False,
        action="store_true",
        help="Disable out files for data store output",
    )

def add_media_source(
    parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup]
) -> None:
    """Add an argument for type."""
    parser.add_argument(
        "-m",
        "--media",
        default=constants.DEFAULT_MEDIA_SOURCE,
        choices=['local', constants.DEFAULT_MEDIA_SOURCE],
        help="Source for fetch media (e.g. local, cloud)",
    )
