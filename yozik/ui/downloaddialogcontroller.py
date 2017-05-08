import os
from datetime import datetime
from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QDesktopServices
from yozik.core import DownloaderThread, Downloader


class DownloadDialogController(QObject):

    def __init__(self, dialog, downloadable_items, parent=None):
        super().__init__(parent)

        self.downloadable_items = downloadable_items
        self.d = dialog

        self.d.downloadButton.clicked.connect(self.download)
        self.d.cancelButton.clicked.connect(self.cancel)
        self.d.finishButton.clicked.connect(self.finish)
        self.d.downloadToBrowseButton.clicked.connect(self.handle_file_dialog)
        self.d.openDestinationButton.clicked.connect(self.open_destination_folder)

        default_download_path = os.path.expanduser("~") + "/yozik/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.d.downloadToInputField.setText(default_download_path)

        self._current_url_index = -1
        self._count_running_threads = 0
        self._thread_pool = []

    def show(self):
        for (title, url) in self.downloadable_items:
            self.d.add_table_row(title, url)
        self.d.exec_()

    def download(self):
        self._remove_trailing_slash()
        if not self._validate_output_directory(self.d.downloadToInputField.text()):
            return

        self._start_next_thread_or_finish(initial=True)

        if len(self.downloadable_items) > 0:
            self._start_next_thread_or_finish(initial=True)

        self.d.exchange_download_with_cancel()

    def cancel(self):
        for thread in self._thread_pool:
            thread.stop()
        self.finish()

    def finish(self):
        self.d.close()

    def handle_file_dialog(self):
        directory = QFileDialog.getExistingDirectory(caption='Select download path', parent=self.d)
        self.d.downloadToInputField.setText(directory)

    def open_destination_folder(self):
        QDesktopServices.openUrl(QUrl(self.d.downloadToInputField.text()))

    def _remove_trailing_slash(self):
        text = self.d.downloadToInputField.text()
        if text == "/":
            return
        if text.endswith("/"):
            self.d.downloadToInputField.setText(text[:-1])
        return

    def _validate_output_directory(self, directory):
        if os.path.isdir(directory) and os.access(directory, os.W_OK):
            return True
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                if not os.access(directory, os.W_OK):
                    raise OSError("Directory not writable")
                return True
            except (OSError, IOError):
                dlg = QMessageBox()
                dlg.setText("Directory %s cannot be created or is not writable" % directory)
                dlg.setIcon(QMessageBox.Critical)
                dlg.exec_()
                return False

    def _start_next_thread_or_finish(self, initial=False):
        if initial is False:
            self._count_running_threads -= 1
            self._thread_pool.pop(0)

        if len(self.downloadable_items) == 0 and self._count_running_threads == 0:
            self.d.exchange_cancel_with_finish()
            return
        elif len(self.downloadable_items) == 0:
            return

        self._current_url_index += 1
        self._start_thread(self.downloadable_items.pop(0)[1], self._current_url_index)

    def _start_thread(self, url, index):
        downloader = Downloader(
            url,
            path=self.d.downloadToInputField.text(),
            convert_to=self.d.formatCombobox.currentText(),
            parent=self,
            identifer=index
        )
        thread = DownloaderThread(downloader, index, self)
        postprocessor_handler = PostprocessorProgressHandler(self.d, index, parent=self)

        thread.downloadProgress.connect(self.d.table.cellWidget(index, 2).setValue)
        thread.postprocessorProgress.connect(postprocessor_handler.handle_postprocessor_progress)
        thread.finished.connect(self._start_next_thread_or_finish)
        self._count_running_threads += 1
        self._thread_pool.append(thread)
        thread.start()


class PostprocessorProgressHandler(QObject):
    def __init__(self, dialog, row_index, parent=None):
        super().__init__(parent)
        self.dialog = dialog
        self.row_index = row_index

    def handle_postprocessor_progress(self, value):
        if value == 10.0:
            self.dialog.show_postprocessor_progress(self.row_index)
        elif value == 100.0:
            self.dialog.hide_postprocessor_progress(self.row_index)

