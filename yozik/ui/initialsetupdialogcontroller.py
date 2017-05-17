from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QProgressDialog
from yozik.core import YoutubeDl, FFmpeg
from yozik.core import ThirdpartySoftwareThread


class InitialSetupDialogController(QObject):
    def __init__(self, dialog, parent=None):
        super().__init__(parent=parent)
        self.d = dialog
        self.thirdpartysoftware = self._init_software()

        self.d.downloadButton.clicked.connect(self.download)
        self.pd = None

    def _init_software(self):
        return [YoutubeDl(), FFmpeg()]

    def populate_versions(self):
        for software in self.thirdpartysoftware:
            self.d.add_row(
                name=software.name(),
                installed_version=software.installed_version(),
                available_version=software.available_version()
            )

    def download(self):
        self.pd = QProgressDialog("Downloading and installing packages...", "Abort", 0, 0, parent=self.d)
        self.pd.setMinimumDuration(1)
        self.pd.setAutoClose(False)
        self.pd.setAutoReset(False)

        thread = ThirdpartySoftwareThread(self.thirdpartysoftware, parent=self)
        thread.finished.connect(self._finished)
        thread.started.connect(self._started)
        thread.start()


    def close(self):
        pass


    def _started(self):
        print("somthing started")

    def _finished(self):
        print("thread finished")
        self.d.table.setRowCount(0)
        self._init_software()
        self.populate_versions()

        self.pd.setValue(100)
        self.pd.reset()
        self.pd.hide()
        self.pd = None


