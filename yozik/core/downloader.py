from PyQt5.QtCore import QObject, pyqtSignal
import youtube_dl
import re


class Downloader(QObject):
    FORMAT_AUDIO_MP3 = 'mp3'
    FORMAT_AUDIO_OGG = 'ogg'
    FORMAT_VIDEO_KEEP_ORIGINAL = 'keep original format'
    FORMAT_VIDEO_MP4 = 'mp4'
    FORMAT_VIDEO_WEBM = 'webm'
    FORMAT_VIDEO_MKV = 'mkv'

    AUDIO_FORMATS = (FORMAT_AUDIO_MP3, FORMAT_AUDIO_OGG)
    VIDEO_FORMATS = (FORMAT_VIDEO_KEEP_ORIGINAL, FORMAT_VIDEO_MP4, FORMAT_VIDEO_WEBM, FORMAT_VIDEO_MKV)

    downloadProgress = pyqtSignal(float)
    postprocessorProgress = pyqtSignal(float)

    def __init__(self, url, path="", convert_to=None, parent=None, identifer=None):
        super().__init__(parent)

        if convert_to not in Downloader.AUDIO_FORMATS + Downloader.VIDEO_FORMATS:
            raise AttributeError("%s is not supported conversion format" % convert_to)

        self.convert_to = convert_to
        self.url = url
        self.path = path
        self.identifier = identifer
        self.temp_files = set()

    def download(self):
        ydl_opts = self._download_options()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def postprocessing_started(self, destination_filename=None):
        if destination_filename:
            self.temp_files.add(destination_filename)
        self.postprocessorProgress.emit(10.0)

    def postprocessing_finished(self):
        self.postprocessorProgress.emit(100.0)

    def _progress_hook(self, d):
        self.temp_files.add(d['filename'])
        if 'tmpfilename' in d:
            self.temp_files.add(d['tmpfilename'])

        if d['status'] == 'downloading':
            self.downloadProgress.emit(self._percent_str_to_float(d['_percent_str']))
        if d['status'] == 'finished':
            self.downloadProgress.emit(100.0)
            if self.convert_to == Downloader.FORMAT_VIDEO_KEEP_ORIGINAL:
                self.postprocessing_started()
                self.postprocessing_finished()

    def _download_options(self):
        if self.convert_to in Downloader.AUDIO_FORMATS:
            return self._download_options_audio()
        else:
            return self._download_options_video()

    def _download_options_audio(self):
        return {
            'format': 'bestaudio',
            'postprocessors':  [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.convert_to,
                'preferredquality': '256',
            }],
            'outtmpl': self.path + '/' + youtube_dl.DEFAULT_OUTTMPL,
            'logger': DownloadLogger(self),
            'progress_hooks': [self._progress_hook],
        }

    def _download_options_video(self):
        options = {
            'format': 'best',
            'outtmpl': self.path + '/' + youtube_dl.DEFAULT_OUTTMPL,
            'logger': DownloadLogger(self),
            'progress_hooks': [self._progress_hook],
        }

        if self.convert_to == Downloader.FORMAT_VIDEO_KEEP_ORIGINAL:
            return options
        else:
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.convert_to
            }]
            return options

    def _percent_str_to_float(self, percent_str):
        return float(percent_str[:-1])


class DownloadLogger(object):
    def __init__(self, downloader):
        self.downloader = downloader

    def debug(self, msg):
        if msg.startswith("[ffmpeg] Destination:"):
            filename = msg.replace("[ffmpeg] Destination:", "").strip()
            self.downloader.postprocessing_started(filename)
        elif msg.startswith("Deleting original file"):
            self.downloader.postprocessing_finished()
        elif msg.startswith("[ffmpeg] Not converting video file "):
            filename = msg.replace("[ffmpeg] Not converting video file ", "")\
                .replace(" - already is in target format mp4", "")\
                .strip()
            self.downloader.postprocessing_started(filename)
            self.downloader.postprocessing_finished()
        elif msg.startswith("[ffmpeg] Converting video from"):
            filename = re.search('Destination: (.)+$', msg).group(1).strip()
            self.downloader.postprocessing_started(filename)
        return

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

