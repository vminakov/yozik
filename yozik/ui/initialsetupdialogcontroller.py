from PyQt5.QtCore import QObject, QUrl
from yozik.core.thirdpartysoftware import YoutubeDl, FFmpeg


class InitialSetupDialogController(QObject):
    def __init__(self, dialog, parent=None):
        super().__init__(parent=parent)
        self.d = dialog
        self.thirdaprtysoftware = [YoutubeDl(), FFmpeg()]

        self.d.downloadButton.clicked.connect(self.download)

    def populate_versions(self):
        for software in self.thirdaprtysoftware:
            self.d.add_row(
                name=software.name(),
                installed_version=software.installed_version(),
                available_version=software.available_version()
            )

    def download(self):
        self.thirdaprtysoftware[1].download()
        self.thirdaprtysoftware[1].install()

    def close(self):
        pass
