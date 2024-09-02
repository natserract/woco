import argparse
import os
from typing import List

from woco.cli import SubParsersAction
from woco.cli.arguments.run import set_run_arguments
from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import read_config_file

def add_subparser(
    subparsers: SubParsersAction, parents: List[argparse.ArgumentParser]
) -> None:
    run_parser = subparsers.add_parser(
        "run",
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=parents,
        help="Starts Woco CLI",
    )
    run_parser.set_defaults(func=run)
    set_run_arguments(run_parser)

def run(args: argparse.Namespace) -> None:
    try:
        root_dir = os.path.join('.')
        woco_configs = get_data_files([root_dir], is_config_file)
        if len(woco_configs) == 0:
            raise SystemError("Can't get config.yml file. Please make sure the config file is exist!")

        read_yml_files = read_config_file(woco_configs[0])
        print('read_yml_files', read_yml_files)
    except Exception as ex:
        raise ValueError(ex)
