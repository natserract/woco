import os
import re
import sys
import logging
import logging.config
from typing import (
    Optional,
    Text,
    Union,
    overload,
    Literal
)
from pathlib import Path
import woco.config as cfg
from woco.shared.constants import DEFAULT_CONFIG_PATH

logger = logging.getLogger(__name__)

def configure_logging(
    log_level: Optional[int] = None,
) -> None:
    _log_level = log_level
    if _log_level is None:
        _log_level = logging.getLevelName(cfg.DEFAULT_LOG_LEVEL)

    logging.getLogger(__name__).setLevel(_log_level)

@overload
def get_validated_path(
    current: Optional[Union["Path", Text]],
    parameter: Text,
    default: Optional[Union["Path", Text]] = ...,
    none_is_valid: "Literal[False]" = ...,
) -> Union["Path", Text]:
    ...


@overload
def get_validated_path(
    current: Optional[Union["Path", Text]],
    parameter: Text,
    default: Optional[Union["Path", Text]] = ...,
    none_is_valid: "Literal[True]" = ...,
) -> Optional[Union["Path", Text]]:
    ...

def get_validated_path(
    current: Optional[Union["Path", Text]],
    parameter: Text,
    default: Optional[Union["Path", Text]] = None,
    none_is_valid: bool = False,
) -> Optional[Union["Path", Text]]:
    """Checks whether a file path or its default value is valid and returns it.

    Args:
        current: The parsed value.
        parameter: The name of the parameter.
        default: The default value of the parameter.
        none_is_valid: `True` if `None` is valid value for the path,
                        else `False``

    Returns:
        The current value if it was valid, else the default value of the
        argument if it is valid, else `None`.
    """
    if current is None or current is not None and not os.path.exists(current):
        if default is not None and os.path.exists(default):
            reason_str = f"'{current}' not found."
            if current is None:
                reason_str = f"Parameter '{parameter}' not set."
            else:
                print(
                    f"The path '{current}' does not seem to exist. Using the "
                    f"default value '{default}' instead."
                )

            logger.debug(f"{reason_str} Using default location '{default}' instead.")
            current = default
        elif none_is_valid:
            current = None
        else:
           cancel_cause_not_found(current, parameter, default)

    return current

def cancel_cause_not_found(
    current: Optional[Union["Path", Text]],
    parameter: Text,
    default: Optional[Union["Path", Text]],
) -> None:
    """Exits with an error because the given path was not valid.

    Args:
        current: The path given by the user.
        parameter: The name of the parameter.
        default: The default value of the parameter.

    """
    default_clause = ""
    if default:
        default_clause = f"use the default location ('{default}') or "
    print(
        "The path '{}' does not exist. Please make sure to {}specify it"
        " with '--{}'.".format(current, default_clause, parameter)
    )
    sys.exit(1)


def validate_config_path(
    config: Optional[Union[Text, "Path"]],
    default_config: Text = DEFAULT_CONFIG_PATH,
) -> Text:
    """Verifies that the config path exists.

    Exit if the config file does not exist.

    Args:
        config: Path to the config file.
        default_config: default config to use if the file at `config` doesn't exist.

    Returns: The path to the config file.
    """
    config = get_validated_path(config, "config", default_config)

    if not config or not os.path.exists(config):
        print(
            "The config file '{}' does not exist. Use '--config' to specify a "
            "valid config file."
            "".format(config)
        )
        sys.exit(1)

    return str(config)

def get_validated_config(
    config: Optional[Union[Text, "Path"]],
    default_config: Text = DEFAULT_CONFIG_PATH,
) -> Text:
    """Validates config and returns path to validated config file."""
    config = validate_config_path(config, default_config)

    return config

def normalize_name(name: str):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)
