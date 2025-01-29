import os
import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from .installer_ui import Ui_Form
from .utils import get_classisland_path, download_and_extract_classisland
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFontDatabase, QFont
from . import installer_ui_rc  # 此处直接导入qrc转换后的py文件

fontDb = QFontDatabase()
fontID = fontDb.addApplicationFont(":/HarmonyOS_Sans_SC_Regular.ttf")  # 此处的路径为qrc文件中的字体路径
fontFamilies = fontDb.applicationFontFamilies(fontID)

class DownloadThread(QThread):
    progress = pyqtSignal(int)

    def run(self):
        download_and_extract_classisland(self.progress)

class Installer(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setFont(QFont('Harmony Sans'))
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint)
        self.setFixedSize(self.size())
        if not self.is_supported_os():
            QMessageBox.critical(self, "不支持的操作系统", "该计算机不支持ClassIsland。")
            self.close()
            # sys.exit(0)

        exe_path = os.path.join(get_classisland_path(), "ClassIsland.exe")
        if os.path.exists(exe_path):
            self.progressBar.setValue(100)
            subprocess.Popen([exe_path])
            # sys.exit(0)
        else:
            self.progressBar.setValue(0)
            self.download_thread = DownloadThread()
            self.download_thread.progress.connect(self.update_progress)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()

    def is_supported_os(self):
        if sys.platform != "win32":
            return False
        version = sys.getwindowsversion()
        return version.major >= 10

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def on_download_finished(self):
        exe_path = os.path.join(get_classisland_path(), "ClassIsland.exe")
        subprocess.Popen([exe_path])
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = Installer()
    installer.show()
    sys.exit(app.exec_())