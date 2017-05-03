from .searchterm import SearchTerm


class Search(object):
    __instance = None

    def __new__(cls, searchterms):
        if Search.__instance is None:
            Search.__instance = object.__new__(cls)
            Search.__instance.search_results_cache = dict()
        return Search.__instance

    def __init__(self, searchterms):
        if (type(searchterms) != list):
            searchterms = list(searchterms)

        self.searchterms = searchterms
        self.search_results = dict()

    def search(self):
        for searchterm in self.searchterms:
            try:
                self.search_results[searchterm] = self._fetch_from_cache(searchterm)
            except KeyError:
                self.search_results[searchterm] \
                    = self.search_results_cache[searchterm] \
                    = self._fetch_from_youtube(searchterm)

        return self.search_results

    def _fetch_from_cache(self, searchterm):
        return self.search_results_cache[searchterm]

    def _fetch_from_youtube(self, searchterm):
        return SearchTerm.factory(searchterm).results()


