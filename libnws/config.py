import os
import configparser
import logging
from pathlib import Path
logger = logging.getLogger(__name__)


DEFAULT_CONFIG_PATH = Path(os.path.expanduser("~")) / '.config/nws/nws.conf'
DEFAULT_EXPORT_DIR = Path(os.path.expanduser("~")) / 'nws_exports/'


class ConfigManager:
    """An abstraction for managing a persistent user configuration file"""
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.config_root = Path(self.config_path).parent
        if not os.path.isfile(self.config_path):
            Path(self.config_root).mkdir(parents=True, exist_ok=True)
            self._init_new_user_config()
        else:
            self.config.read(self.config_path)
    
    def _init_new_user_config(self):
        self.config['nws'] = {
            'address':              '1600 Pennsylvania Avenue NW, Washington, DC 20500',
            'measurements':         'imperial',
            'cache_api_responses':  True,
            'exports_dir':          DEFAULT_EXPORT_DIR,
        }
        self.save_settings()

    def get_all(self) -> dict:
        return self.config.items('nws')
    
    def get(self, setting: str) -> str | None:
        return self.config['nws'].get(setting)
    
    def set(self, setting: str, value: str) -> bool:
        if setting not in self.config['nws']:
            return False
        self.config['nws'][setting] = value
        self.save_settings()
        return True

    def save_settings(self):
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)
        logger.debug(f'Saved settings to {self.config_path}')
