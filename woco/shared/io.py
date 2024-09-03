from typing import Any, Dict, List, Optional, Text, Type, Union
from pathlib import Path
import json
import os

from ruamel import yaml as yaml

DEFAULT_ENCODING = "utf-8"
YAML_VERSION = (1, 2)

def read_validated_yaml(
    filename: Union[Text, Path],
    reader_type: Union[Text, List[Text]] = "safe",
) -> Any:
    """Validates YAML file content and returns parsed content.

    Args:
        filename: The path to the file which should be read.
        schema: The path to the schema file which should be used for validating the
            file content.
        reader_type: Reader type to use. By default "safe" will be used.

    Returns:
        The parsed file content.

    Raises:
        YamlValidationException: In case the model configuration doesn't match the
            expected schema.
    """
    content = read_file(filename)
    return read_yaml(content, reader_type)

def read_config_file(
    filename: Union[Path, Text], reader_type: Union[Text, List[Text]] = "safe"
)-> Dict[Text, Any]:
    """Parses a yaml configuration file. Content needs to be a dictionary.

    Args:
        filename: The path to the file which should be read.
        reader_type: Reader type to use. By default "safe" will be used.

    Raises:
        YamlValidationException: In case file content is not a `Dict`.

    Returns:
        Parsed config file.
    """
    return read_validated_yaml(filename, reader_type)

def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""
    try:
        with open(filename, encoding=encoding) as f:
            return f.read()
    except Exception as ex:
        raise LookupError(
            f"Failed to read file, " f"'{os.path.abspath(filename)}'"
        )

def read_json_file(filename: Union[Text, Path]) -> Any:
    """Read json from a file."""
    content = read_file(filename)
    try:
        return json.loads(content)
    except ValueError as ex:
        raise ValueError(
            f"Failed to read json from '{os.path.abspath(filename)}'. Error: {ex}"
        )

def read_yaml(content: Text, reader_type: Union[Text, List[Text]] = "safe") -> Any:
    """Parses yaml from a text.

    Args:
        content: A text containing yaml content.
        reader_type: Reader type to use. By default "safe" will be used.

    Raises:
        ruamel.yaml.parser.ParserError: If there was an error when parsing the YAML.
    """
    if _is_ascii(content):
        # Required to make sure emojis are correctly parsed
        content = (
            content.encode("utf-8")
            .decode("raw_unicode_escape")
            .encode("utf-16", "surrogatepass")
            .decode("utf-16")
        )

    yaml_parser = yaml.YAML(typ=reader_type)
    yaml_parser.version = YAML_VERSION  # type: ignore[assignment]
    yaml_parser.preserve_quotes = True  # type: ignore[assignment]

    return yaml_parser.load(content) or {}

def write_text_file(
    content: Text,
    file_path: Union[Text, Path],
    encoding: Text = DEFAULT_ENCODING,
    append: bool = False,
) -> None:
    """Writes text to a file.

    Args:
        content: The content to write.
        file_path: The path to which the content should be written.
        encoding: The encoding which should be used.
        append: Whether to append to the file or to truncate the file.

    """
    mode = "a" if append else "w"
    with open(file_path, mode, encoding=encoding) as file:
        file.write(content)

def dump_obj_as_json_to_file(filename: Union[Text, Path], obj: Any) -> None:
    """Dump an object as a json string to a file."""
    write_text_file(json.dumps(obj, ensure_ascii=False, indent=2), filename)

def _is_ascii(text: Text) -> bool:
    return all(ord(character) < 128 for character in text)
