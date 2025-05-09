import sys
import os
from PyQt5.QtWidgets import QApplication

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ui.main_window import MainWindow
from src.utils.settings_manager import SettingsManager

CONFIG_FILE = 'config.json'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings_manager = SettingsManager(CONFIG_FILE)
    main_win = MainWindow(settings_manager)
    main_win.show()
    sys.exit(app.exec_())
