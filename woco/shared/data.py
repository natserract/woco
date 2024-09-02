import os
from pathlib import Path
from typing import Text, Optional, Union, List, Callable, Set, Iterable

JSON_FILE_EXTENSIONS = [".json"]
YAML_FILE_EXTENSIONS = [".yml", ".yaml"]
DATA_EXTENSIONS = set(JSON_FILE_EXTENSIONS + YAML_FILE_EXTENSIONS)

def yaml_file_extension() -> Text:
    """Return YAML file extension."""
    return YAML_FILE_EXTENSIONS[0]


def is_likely_yaml_file(file_path: Union[Text, Path]) -> bool:
    """Check if a file likely contains yaml.

    Arguments:
        file_path: path to the file

    Returns:
        `True` if the file likely contains data in yaml format, `False` otherwise.
    """
    return Path(file_path).suffix in set(YAML_FILE_EXTENSIONS)

def is_likely_json_file(file_path: Text) -> bool:
    """Check if a file likely contains json.

    Arguments:
        file_path: path to the file

    Returns:
        `True` if the file likely contains data in json format, `False` otherwise.
    """
    return Path(file_path).suffix in set(JSON_FILE_EXTENSIONS)

def is_config_file(file_path: Text) -> bool:
    """Checks whether the given file path is a Woco config file.

    Args:
        file_path: Path of the file which should be checked.

    Returns:
        `True` if it's a Woco config file, otherwise `False`.
    """
    file_name = os.path.basename(file_path)

    return file_name in ["config.yml", "config.yaml"]

def get_data_files(
    paths: Optional[Union[Text, List[Text]]], filter_predicate: Callable[[Text], bool]
) -> List[Text]:
    data_files = set()

    if paths is None:
        paths = []
    elif isinstance(paths, str):
        paths = [paths]

    for path in set(paths):
        if not path:
            continue

        if is_valid_filetype(path):
            if filter_predicate(path):
                data_files.add(os.path.abspath(path))
        else:
            new_data_files = _find_data_files_in_directory(path, filter_predicate)
            data_files.update(new_data_files)

    return sorted(data_files)

def _find_data_files_in_directory(
    directory: Text, filter_property: Callable[[Text], bool]
) -> Set[Text]:
    filtered_files = set()

    for root, _, files in os.walk(directory, followlinks=True):
        # we sort the files here to ensure consistent order for repeatable training
        # results
        for f in sorted(files):
            full_path = os.path.join(root, f)

            if not is_valid_filetype(full_path):
                continue

            if filter_property(full_path):
                filtered_files.add(full_path)

    return filtered_files

def is_valid_filetype(path: Union[Path, Text]) -> bool:
    """Checks if given file has a supported extension.

    Args:
        path: Path to the source file.

    Returns:
        `True` is given file has supported extension, `False` otherwise.
    """
    return Path(path).is_file() and Path(path).suffix in DATA_EXTENSIONS
