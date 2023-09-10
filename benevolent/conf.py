from configparser import ConfigParser
from pathlib import Path
from typing import Optional


def config_file_path() -> Path:
    """Returns the path to the config file"""
    return Path("benevolent.conf")


def create_config(tesseract_path: str) -> None:
    """Creates the config file for tesseract."""
    with open(config_file_path(), "w") as config_file:
        config_file.write("[tesseract]\n")
        config_file.write(f"path={tesseract_path}")


def get_config() -> Optional[ConfigParser]:
    """Parses the config file"""
    path = config_file_path()
    if not path.exists():
        return None
    cfg = ConfigParser()
    cfg.read(path)
    return cfg
