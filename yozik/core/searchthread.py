from PyQt5.QtCore import QThread, pyqtSignal


class SearchThread(QThread):
    searchTermStarted = pyqtSignal(int, int)
    searchTermFinished = pyqtSignal(str, list)

    def __init__(self, search, parent=None):
        super().__init__(parent)
        self._search = search
        self._search_results = []

    def __del__(self):
        self.wait()

    def run(self):
        self._search.searchTermStarted.connect(self._search_term_started)
        self._search.searchTermFinished.connect(self._search_term_finished)

        self._search_results = self._search.search()

    def _search_term_started(self, index, total):
        self.searchTermStarted.emit(index, total)

    def _search_term_finished(self, searchterm, search_results):
        self.searchTermFinished.emit(searchterm, search_results)

    def search_results(self):
        return self._search_results

    def stop(self):
        self.terminate()

