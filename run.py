#!/usr/bin/env python3
from os.path import expanduser

import sys
sys.path.append(expanduser("~") + "/.config/yozik/youtube-dl")


def check_for_youtube_dl():
    try:
        import youtube_dl
        return True
    except ImportError:
        return False


def start_main_app():
    from PyQt5.QtWidgets import QApplication, qApp
    from yozik.ui import MainWindowController, MainWindow
    app = QApplication(sys.argv)
    qApp.setApplicationDisplayName("Yozik")
    qApp.setApplicationName("Yozik")

    w = MainWindow()
    c = MainWindowController(w)
    w.show()
    sys.exit(app.exec_())


def start_dependency_downloader():
    from PyQt5.QtWidgets import QApplication, qApp
    import yozik.ui.initialsetupdialog
    app = QApplication(sys.argv)
    qApp.setApplicationDisplayName("Yozik")
    qApp.setApplicationName("Yozik")

    w = yozik.ui.initialsetupdialog.InitialSetupDialog()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    if check_for_youtube_dl():
        start_main_app()
    else:
        start_dependency_downloader()




