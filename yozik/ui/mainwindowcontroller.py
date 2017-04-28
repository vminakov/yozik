from PyQt5.QtCore import QObject
from yozik.core import Search, SearchThread
from yozik.ui import DownloadAudioDialogController, DownloadAudioDialog


class MainWindowController(QObject):
    def __init__(self, mainwindow):
        super().__init__()

        self.w = mainwindow
        self.w.findButton.clicked.connect(self.find)
        self.w.clearButton.clicked.connect(self.clear)
        self.w.downloadButton.clicked.connect(self.show_download_dialog)
        self._search_thread = None

    def clear(self):
        self.w.treeView.clear()
        self.w.inputField.clear()

    def find(self):
        self.w.treeView.clear()
        self.w.toggle_loading_spinner()
        search_terms = self._sanitize_input(self.w.inputField.toPlainText())

        youtube_search = Search(search_terms)
        self._search_thread = SearchThread(youtube_search, parent=self)
        self._search_thread.finished.connect(self._populate_search_results)
        self._search_thread.start()

    def show_download_dialog(self):
        downloadable_items = self._downloadable_items()
        if len(downloadable_items) == 0:
            return

        dialog_controller = DownloadAudioDialogController(
            DownloadAudioDialog(self.w),
            downloadable_items,
            self.w
        )
        dialog_controller.show()

    def _populate_search_results(self):
        results = self._search_thread.search_results()
        for searchterm, downloadUrls in results.items():
            first_search_result = downloadUrls.pop(0)
            parent_row = self.w.add_parent_row(searchterm, first_search_result[0], first_search_result[1])
            for search_result in downloadUrls:
                self.w.add_child_row(parent_row, searchterm, search_result[0], search_result[1])

        self.w.toggle_loading_spinner()

    def _downloadable_items(self):
        return self._extract_top_level_checked_items()

    def _extract_top_level_checked_items(self):
        checked_items = []
        for i in range(self.w.treeView.topLevelItemCount()):
            top_item = self.w.treeView.topLevelItem(i)
            if top_item.isChecked():
                checked_items.append(
                    (top_item.title(), top_item.url())
                )

            checked_items.extend(self._extract_child_checked_items(top_item))

        return checked_items

    def _extract_child_checked_items(self, tree_item):
        checked_items = []
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            if child_item.isChecked():
                checked_items.append(
                    (child_item.title(), child_item.url())
                )
        return checked_items

    def _sanitize_input(self, text):
        search_terms = text.splitlines()
        search_terms = list(filter(None, search_terms))

        return search_terms
