import argparse
import os
from typing import List

from woco.cli import SubParsersAction
from woco.cli.arguments.run import set_run_arguments
from woco.shared.data import get_data_files, is_config_file
from woco.shared.io import read_config_file
from woco.shared.utils import get_validated_config
from woco.workflow import Workflow

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
        config = get_validated_config(args.config)
        workflow = Workflow(
            options={
                'disable_out_file': args.disable_out_file,
                'media_source': args.media,
            }
        )
        workflow.run_workflow(config_path=config)
    except Exception as ex:
        raise ValueError(ex)
