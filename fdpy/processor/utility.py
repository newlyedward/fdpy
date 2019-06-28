import json
from pathlib import Path
from typing import Any


def _get_processor_dir(temp_name: str):
    """
    Get path where processor is running in.
    :param temp_name:
    :return:
    """
    cwd = Path.cwd()
    temp_path = cwd.joinpath(temp_name)

    # if .fdprocessor folder exists in current working directory,
    # then use it as processor running path
    if temp_path.exists():
        return cwd, temp_path

    # otherwise use home path of system
    home_path = Path.home()
    temp_path = home_path.joinpath(temp_name)

    # Create .fdprocessor folder under home path if not exist
    if not temp_path.exists():
        temp_path.mkdir()

    return home_path, temp_path


PROCESSOR_DIR, TEMP_DIR = _get_processor_dir(".fdprocessor")


def get_file_path(filename: str):
    """
    Get path for temp file with filename.
    """
    return TEMP_DIR.joinpath(filename)


def get_folder_path(folder_name: str):
    """
    Get path for temp file with filename.
    :param folder_name:
    :return:
    """
    folder_path = TEMP_DIR.joinpath(folder_name)

    if not folder_path.exists():
        folder_path.mkdir()

    return folder_path


def load_json(filename: Any):
    """
    Load data from json file in temp path.
    :param filename: str or Path
    """
    if isinstance(filename, str):
        filepath = get_file_path(filename)
    elif isinstance(filename, Path):
        filepath = filename
    else:
        return {}

    if filepath.exists():
        with open(filepath, mode="r", encoding="UTF-8") as f:
            data = json.load(f)
        return data
    else:
        save_json(filename, {})
        return {}


def save_json(filename: str, data: dict):
    """
    Save data into json file in temp path.
    """
    filepath = get_file_path(filename)
    with open(filepath, mode="w+", encoding="UTF-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )
