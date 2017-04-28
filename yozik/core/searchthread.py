from PyQt5.QtCore import QThread, pyqtSignal


class SearchThread(QThread):

    def __init__(self, search, parent=None):
        super().__init__(parent)
        self._search = search
        self._search_results = []

    def __del__(self):
        self.wait()

    def run(self):
        self._search_results = self._search.search()

    def search_results(self):
        return self._search_results

    def stop(self):
        self.terminate()

