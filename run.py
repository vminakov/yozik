#!/usr/bin/env python3
from os.path import expanduser

import sys
sys.path.insert(0, expanduser("~") + "/.config/yozik/thirdpartysoftware/youtube-dl/youtube-dl")


def check_for_youtube_dl():
    return False
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
    from yozik.ui import InitialSetupDialogController, InitialSetupDialog
    app = QApplication(sys.argv)
    qApp.setApplicationDisplayName("Yozik")
    qApp.setApplicationName("Yozik")

    w = InitialSetupDialog()
    c = InitialSetupDialogController(w)
    w.show()
    c.populate_versions()

    sys.exit(app.exec_())


if __name__ == '__main__':
    if check_for_youtube_dl():
        start_main_app()
    else:
        start_dependency_downloader()




