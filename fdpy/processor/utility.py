from pathlib import Path


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
