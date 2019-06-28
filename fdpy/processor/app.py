from abc import ABC


class BaseApp(ABC):
    """
    Abstract class for app.
    """

    app_name = ""           # Unique name used for creating engine and widget
    app_module = ""         # App module string used in import module
    app_path = ""           # Absolute path of app folder
    engine_class = None     # App engine class

