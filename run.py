#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, qApp
from yozik.ui import MainWindowController, MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qApp.setApplicationDisplayName("Yozik")
    qApp.setApplicationName("Yozik")

    w = MainWindow()
    c = MainWindowController(w)

    w.show()

    sys.exit(app.exec_())