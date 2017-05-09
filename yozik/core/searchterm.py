import abc
import youtube_dl
import re


class SearchTerm(metaclass=abc.ABCMeta):
    YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v="
    YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list="

    YOUTUBE_DL_DEFAULT_OPTIONS = {"nocheckcertificate": True, "ignoreerrors": True}

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
        """Retrieve list of link pairs (tuples of URL and title)"""

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
        with youtube_dl.YoutubeDL(self.YOUTUBE_DL_DEFAULT_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return [(video_url, info['title'])]


class PlaylistLink(SearchTerm):
    def _search(self):
        search_results = []
        playlist_url = self.YOUTUBE_PLAYLIST_URL + self._searchterm
        with youtube_dl.YoutubeDL(self.YOUTUBE_DL_DEFAULT_OPTIONS) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            for info in playlist_info['entries']:
                try:
                    search_results.append(
                        (info['webpage_url'], info['title'])
                    )
                except TypeError:
                    # Happens when youtube-dl didn't return anything (e.g. video is blocked in the country)
                    pass

        return search_results


class SimpleSearchTerm(SearchTerm):
    def _search(self):
        search_results = []
        search_url = "ytsearch10: " + self._searchterm
        with youtube_dl.YoutubeDL(self.YOUTUBE_DL_DEFAULT_OPTIONS) as ydl:
            search_info = ydl.extract_info(search_url, download=False)
            for info in search_info['entries']:
                search_results.append(
                    (info['webpage_url'], info['title'])
                )

        return search_results