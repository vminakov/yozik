from lxml.html import html5parser, tostring
import abc
import lxml.html
import urllib
import youtube_dl
import re


class SearchTerm(metaclass=abc.ABCMeta):
    YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v="
    YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list="

    def __init__(self, searchterm):
        self._searchterm = searchterm
        self._links = []

    def results(self):
        if len(self._links) == 0:
            self._links = self._search()
        return self._links

    def searchterm(self):
        return self._searchterm

    @abc.abstractmethod
    def _search(self):
        """Retrieve links (tuples of URL and title)"""

    @staticmethod
    def factory(searchterm):
        video_pattern = re.compile("watch\?v=([^&]+)")
        playlist_pattern = re.compile("(\?|&)list=([^&]+)")

        if playlist_pattern.search(searchterm):
            return PlaylistLink(playlist_pattern.search(searchterm).group(2))
        elif video_pattern.search(searchterm):
            return DirectLink(video_pattern.search(searchterm).group(1))
        else:
            return SimpleSearchTerm(searchterm)


class DirectLink(SearchTerm):
    def _search(self):
        video_url = self.YOUTUBE_VIDEO_URL + self._searchterm
        with youtube_dl.YoutubeDL({"ignoreerrors": True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return [(video_url, info['title'])]


class PlaylistLink(SearchTerm):
    def _search(self):
        search_results = []
        playlist_url = self.YOUTUBE_PLAYLIST_URL + self._searchterm
        with youtube_dl.YoutubeDL({"ignoreerrors": True}) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            for info in playlist_info['entries']:
                search_results.append(
                    (info['webpage_url'], info['title'])
                )

        return search_results


class SimpleSearchTerm(SearchTerm):
    def _search(self):
        search_results = []

        youtube_search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(self._searchterm)
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
        return self.YOUTUBE_VIDEO_URL + link.get("href")
