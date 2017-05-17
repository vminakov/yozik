import abc
import sys
import requests
import os
import tarfile
import re
import platform
import shutil
import glob
from shutil import rmtree
from os.path import expanduser
from urllib.request import urlretrieve
from subprocess import check_output, call


class ThirdpartySoftware(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def name(self):
        """Returns name of the software package"""

    @abc.abstractmethod
    def is_installed(self):
        """Returns True/False if concrete sofware is installed"""

    @abc.abstractmethod
    def is_update_available(self):
        """Returns True/False if software update is available"""

    @abc.abstractmethod
    def installed_version(self):
        """Return version label of currently installed software or None if not installed"""

    @abc.abstractmethod
    def available_version(self):
        """Return version label of next avaialble version"""

    @abc.abstractmethod
    def download(self):
        """Download next availabe version"""

    @abc.abstractmethod
    def install(self):
        """Installs downloaded version"""


class YoutubeDl(ThirdpartySoftware):
    INSTALL_PATH = expanduser("~") + "/.config/yozik/thirdpartysoftware/youtube-dl/"
    DOWNLOAD_PATH = INSTALL_PATH + "downloads/"
    DOWNLOAD_FILENAME = DOWNLOAD_PATH + "archive.tar.gz"

    GITHUB_API_ENDPOINT = "https://api.github.com/repos/rg3/youtube-dl/releases"

    @staticmethod
    def register_path():
        if YoutubeDl.INSTALL_PATH not in sys.path:
            sys.path.append(YoutubeDl.INSTALL_PATH + "/youtube-dl")

    def __init__(self):
        YoutubeDl.register_path()
        self._is_installed = True
        self._tag_name = None
        self._download_url = None

        try:
            import youtube_dl
        except ImportError:
            self._is_installed = False

    def name(self):
        return "youtube-dl"

    def is_installed(self):
        return self._is_installed

    def is_update_available(self):
        if not self.is_installed():
            return True
        else:
            return self.available_version() != self.installed_version() and self.available_version() is not None

    def installed_version(self):
        if not self.is_installed():
            return ""
        else:
            import youtube_dl.version
            return youtube_dl.version.__version__

    def available_version(self):
        if not self._tag_name:
            latest_release = requests.get(self.GITHUB_API_ENDPOINT).json()[0]
            self._tag_name = latest_release['tag_name']
            for release_asset in latest_release['assets']:
                archive_name_pattern = "%s.tar.gz" % self._tag_name
                if release_asset['browser_download_url'].endswith(archive_name_pattern):
                    self._download_url = release_asset['browser_download_url']

        return self._tag_name

    def download(self):
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
        if os.path.exists(self.DOWNLOAD_FILENAME):
            os.unlink(self.DOWNLOAD_FILENAME)

        urlretrieve(self._download_url, self.DOWNLOAD_FILENAME)

        return True

    def install(self):
        try:
            rmtree(self.INSTALL_PATH + "youtube-dl")
        except FileNotFoundError:
            pass

        tar = tarfile.open(self.DOWNLOAD_FILENAME)
        tar.extractall(self.INSTALL_PATH)
        tar.close()


class FFmpeg(ThirdpartySoftware):
    INSTALL_PATH = expanduser("~") + "/.config/yozik/thirdpartysoftware/ffmpeg/"
    FFMPEG_PATH = INSTALL_PATH + "ffmpeg"


    def __init__(self):
        system = platform.system()
        if system == "Darwin":
            self._downloader = _MacOsXDownloader()
        elif system == "Linux":
            self._downloader = _LinuxDownloader()
        else:
            self._downloader = _WindowsDownloader()

    def name(self):
        return "ffmpeg"

    def is_installed(self):
        if os.path.exists(self.FFMPEG_PATH):
            return True
        return False

    def is_update_available(self):
        if not self.is_installed():
            return True
        else:
            return self.available_version() != self.installed_version() and self.available_version() is not None

    def installed_version(self):
        if not self.is_installed():
            return ""

        try:
            version_info = check_output([self.FFMPEG_PATH, '-version']).splitlines()[0]
            version = re.search("(\d\.\d{1,2}(\.\d)?)-", str(version_info)).group(1)
            return version
        except (AttributeError, FileNotFoundError):
            return ""

    def available_version(self):
        return self._downloader.available_version()

    def download(self):
        return self._downloader.download()

    def install(self):
        return self._downloader.install()


# the whole concept of fetching currently available version by checking some websites
# and parsing them with regex's is very dumb. however, there's no other (to my understanding)
# better way to get such info. and parsing HTML with something with lxml and html5lib
# is an overkill for this simple task
class _WindowsDownloader:
    pass

class _LinuxDownloader:
    DOWNLOAD_PAGE = "https://www.johnvansickle.com/ffmpeg/"
    DOWNLOAD_URL_32 = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-32bit-static.tar.xz"
    DOWNLOAD_URL_64 = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz"

    DOWNLOAD_PATH = FFmpeg.INSTALL_PATH + "downloads/"
    DOWNLOAD_FILENAME = DOWNLOAD_PATH + "ffmpeg.tar.xz"

    def __init__(self):
        self._available_version = None
        self._download_url = None

    def available_version(self):
        if not self._available_version:
            try:
                html = str(requests.get(self.DOWNLOAD_PAGE).content)
                version = re.search("release: (\d\.\d{1,2}(\.\d)?)", html).group(1)
                self._available_version = version
                self._download_url = self.DOWNLOAD_URL_64 if self._is_os_64bit() else self.DOWNLOAD_URL_32
            except (AttributeError, requests.exceptions.RequestException) as e:
                print(e)
                return None

        return self._available_version

    def download(self):
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
        if os.path.exists(self.DOWNLOAD_FILENAME):
            os.unlink(self.DOWNLOAD_FILENAME)

        urlretrieve(self._download_url, self.DOWNLOAD_FILENAME)
        return True

    def install(self):
        tar = tarfile.open(self.DOWNLOAD_FILENAME)
        tar.extractall(self.DOWNLOAD_PATH)
        tar.close()

        files = glob.glob(self.DOWNLOAD_PATH + "*")
        files.sort(key=os.path.getmtime)
        extracted_ffmpeg = files[0] + "/ffmpeg"
        shutil.copy2(extracted_ffmpeg, FFmpeg.FFMPEG_PATH)


    def _is_os_64bit(self):
        return platform.machine().endswith('64')

class _MacOsXDownloader:
    # Installing ffmpeg for mac os x is even more hackier. ffmpeg static builds are provided in .dmg or .7z format.
    # The latter is not supported normally by Python - either via external programms that have to be installed manually
    # (p7zip) or pylzma, which for me chrashes on ffmpeg archives. So, .dmg is downloaded, mountend, ffmpeg is copied
    # and then image is demounted.

    DOWNLOAD_PAGE = "https://evermeet.cx/ffmpeg/"
    DOWNLOAD_PATH = FFmpeg.INSTALL_PATH + "downloads/"
    DOWNLOAD_FILENAME = DOWNLOAD_PATH + "ffmpeg.dmg"
    MOUNT_POINT = "/Volumes/ffmpeg"

    def __init__(self):
        self._available_version = None
        self._download_url = None

    def available_version(self):
        if not self._available_version:
            try:
                html = str(requests.get(self.DOWNLOAD_PAGE).content)
                version = re.search("<a href=\"ffmpeg-(\d\.\d{1,2}(\.\d)?)\.dmg\"", html).group(1)
                self._available_version = version
                self._download_url = "%sffmpeg-%s.dmg" % (self.DOwNLOAD_PAGE, version)
            except (AttributeError, requests.exceptions.RequestException) as e:
                print(e)
                return None

        return self._available_version

    def download(self):
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
        if os.path.exists(self.DOWNLOAD_FILENAME):
            os.unlink(self.DOWNLOAD_FILENAME)

        urlretrieve(self._download_url, self.DOWNLOAD_FILENAME)
        return True

    def install(self):
        ret_code = call(['hdiutil', 'attach', '-mountpoint', self.MOUNT_POINT, self.DOWNLOAD_FILENAME])
        if ret_code != 0:
            raise SystemError("Could not mount downloaded ffmpeg image")

        shutil.copy2(os.path.join(self.MOUNT_POINT, 'ffmpeg'), FFmpeg.FFMPEG_PATH)
        ret_code = call(['hdiutil', 'unmount', self.MOUNT_POINT])
        if ret_code != 0:
            raise SystemError("Could not unmount ffmpeg image")







