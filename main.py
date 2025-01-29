import time
import requests
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QWidget, QVBoxLayout, QScrollBar
from loguru import logger

from .utils import download_and_extract_classisland 
import sys
import os
from .installer import Installer

class Plugin:
    def __init__(self, cw_contexts, method):
        self.cw_contexts = cw_contexts
        self.method = method

        self.CONFIG_PATH = f'{cw_contexts["PLUGIN_PATH"]}/config.json'
        self.PATH = cw_contexts['PLUGIN_PATH']
        self.installer_ui = Installer()

    def execute(self):
        """首次执行"""
        self.installer_ui.show()
