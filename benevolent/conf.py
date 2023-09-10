from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir


def config_file_path() -> Path:
    """Returns the path to the config file"""
    return _config_dir() / "benevolent.conf"


def create_config(tesseract_path: str) -> None:
    """Creates the config file for tesseract."""
    if not _config_dir().exists():
        _config_dir().mkdir(parents=True)
    with open(config_file_path(), "w") as config_file:
        config_file.write("[tesseract]\n")
        config_file.write(f"path={tesseract_path}")


def _config_dir() -> Path:
    return Path(user_config_dir("benevolent", "tbd"))


def get_config() -> Optional[ConfigParser]:
    """Parses the config file"""
    path = config_file_path()
    if not path.exists():
        return None
    cfg = ConfigParser()
    cfg.read(path)
    return cfg
