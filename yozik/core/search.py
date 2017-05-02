from lxml.html import html5parser, tostring
import lxml.html
import urllib


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
        search_results = []

        youtube_search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(searchterm)
        el = lxml.html.fromstring(tostring(html5parser.parse(youtube_search_url)))

        for link in el.cssselect("ol.item-section li a.yt-uix-tile-link"):
            if self._is_valid_link(link):
                search_results.append((self._build_download_url(link), link.text))

        return search_results

    def _is_valid_link(self, link):
        if not link.get("href").startswith("/watch?v="):
            return False
        return True

    def _build_download_url(self, link):
        return "https://www.youtube.com" + link.get("href")
