import argparse

from cli.arguments.default_arguments import add_data_param

def set_run_arguments(parser: argparse.ArgumentParser) -> None:
    """Arguments for running Woco directly using `woco run`."""
    add_data_param(parser)
