import argparse
import logging
from typing import Text, Union, Optional

from shared.constants import DEFAULT_DATA_PATH

def add_data_param(
    parser: Union[argparse.ArgumentParser, argparse._ActionsContainer],
    default: Optional[Text] = DEFAULT_DATA_PATH,
    required: bool = False,
    data_type: Text = "Woco ",
) -> None:
    parser.add_argument(
        "--data",
        default=default,
        nargs="+",
        type=str,
        help=f"Paths to the files or directories containing {data_type} data.",
        # The desired behaviour is that required indicates if this argument must
        # have a value, but argparse interprets it as "must have a value
        # from user input", so we toggle it only if our default is not set
        required=required and default is None,
    )

def add_logging_options(parser: argparse.ArgumentParser) -> None:
    """Add options to an argument parser to configure logging levels."""
    logging_arguments = parser.add_argument_group(
        "Python Logging Options",
        "You can control level of log messages printed. "
        "In addition to these arguments, a more fine grained configuration can be "
        "achieved with environment variables. See online documentation for more info.",
    )

    # arguments for logging configuration
    logging_arguments.add_argument(
        "-v",
        "--verbose",
        help="Be verbose. Sets logging level to INFO.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    logging_arguments.add_argument(
        "-vv",
        "--debug",
        help="Print lots of debugging statements. Sets logging level to DEBUG.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    logging_arguments.add_argument(
        "--quiet",
        help="Be quiet! Sets logging level to WARNING.",
        action="store_const",
        dest="loglevel",
        const=logging.WARNING,
    )

    logging_arguments.add_argument(
        "--logging-config-file",
        type=str,
        help="If set, the name of the logging configuration file will be set "
        "to the given name.",
    )
