from PyQt5.QtCore import QThread, pyqtSignal
import os


class DownloaderThread(QThread):
    downloadProgress = pyqtSignal(float)
    postprocessorProgress = pyqtSignal(float)

    def __init__(self, downloader, thread_id=None, parent=None):
        super().__init__(parent)
        self.downloader = downloader
        self._thread_id = thread_id

    def __del__(self):
        self.wait()

    def run(self):
        self.downloader.downloadProgress.connect(self.download_progress_received)
        self.downloader.postprocessorProgress.connect(self.postprocessor_progress_received)
        self.downloader.download()

    def download_progress_received(self, progress):
        self.downloadProgress.emit(progress)

    def postprocessor_progress_received(self, progress):
        self.postprocessorProgress.emit(progress)

    def stop(self):
        self._remove_tmp_files(self.downloader.temp_files)
        self.terminate()

    def _remove_tmp_files(self, filelist):
        for file in filelist:
            try:
                os.remove(file)
            except OSError:
                pass

