from PyQt5.QtCore import pyqtSignal, QObject
from .searchterm import SearchTerm


class Search(QObject):
    __instance = None

    searchTermStarted = pyqtSignal(int, int)
    searchTermFinished = pyqtSignal(str, list)

    def __new__(cls, searchterms, parent=None):
        if Search.__instance is None:
            Search.__instance = QObject.__new__(cls)
            Search.__instance.search_results_cache = dict()
        return Search.__instance

    def __init__(self, searchterms, parent=None):
        super().__init__(parent)
        if (type(searchterms) != list):
            searchterms = list(searchterms)

        self.searchterms = searchterms
        self.search_results = dict()

    def search(self):
        for index, searchterm in enumerate(self.searchterms):
            self.searchTermStarted.emit(index + 1, len(self.searchterms))
            try:
                self.search_results[searchterm] = self._fetch_from_cache(searchterm)
            except KeyError:
                self.search_results[searchterm] \
                    = self.search_results_cache[searchterm] \
                    = self._fetch_from_youtube(searchterm)

            self.searchTermFinished.emit(searchterm, self.search_results[searchterm])

        return self.search_results

    def _fetch_from_cache(self, searchterm):
        return self.search_results_cache[searchterm]

    def _fetch_from_youtube(self, searchterm):
        return SearchTerm.factory(searchterm).results()


