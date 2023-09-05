from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir


def config_file_path() -> Path:
    """Returns the path to the config file"""
    return Path(user_config_dir("benevolent", "tbd")) / "benevolent.conf"


def get_config() -> Optional[ConfigParser]:
    """Parses the config file"""
    path = config_file_path()
    if not path.exists():
        return None
    cfg = ConfigParser()
    cfg.read(path)
    return cfg
