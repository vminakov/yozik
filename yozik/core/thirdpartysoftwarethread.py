from PyQt5.QtCore import QThread, pyqtSignal


class ThirdpartySoftwareThread(QThread):
    def __init__(self, software, parent=None):
        super().__init__(parent)
        self._software = software

    def __del__(self):
        self.wait()

    def run(self):
        for software in self._software:
            software.download()
            software.install()

    def stop(self):
        self.terminate()

