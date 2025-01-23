import time
import requests
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QWidget, QVBoxLayout, QScrollBar
from loguru import logger

from .utils import download_and_extract_classisland 
import sys
import os

class Plugin:
    def __init__(self, cw_contexts, method):
        self.cw_contexts = cw_contexts
        self.method = method

        self.CONFIG_PATH = f'{cw_contexts["PLUGIN_PATH"]}/config.json'
        self.PATH = cw_contexts['PLUGIN_PATH']

    def execute(self):
        """首次执行"""
        classisland_dir = download_and_extract_classisland()
        print("ClassIsland安装成功.")
        os.system(classisland_dir)
        sys.exit(0)
