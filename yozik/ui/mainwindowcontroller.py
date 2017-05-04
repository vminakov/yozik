from PyQt5.QtCore import QObject
from yozik.core import Search, SearchThread
from yozik.ui import DownloadDialogController, DownloadDialog


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
        self.w.toggle_event_processing()
        search_terms = self._sanitize_input(self.w.inputField.toPlainText())

        youtube_search = Search(search_terms)
        self._search_thread = SearchThread(youtube_search, parent=self)
        self._search_thread.searchTermFinished.connect(self._add_search_result)
        self._search_thread.searchTermStarted.connect(self._update_status_bar)
        self._search_thread.finished.connect(self._finish_search)
        self._search_thread.start()

    def show_download_dialog(self):
        downloadable_items = self._downloadable_items()
        if len(downloadable_items) == 0:
            return

        dialog_controller = DownloadDialogController(
            DownloadDialog(self.w),
            downloadable_items,
            self.w
        )
        dialog_controller.show()

    def _update_status_bar(self, index, total):
        self.w.statusBar().showMessage("Processing search term %s from %s" % (index, total))

    def _add_search_result(self, searchterm, search_results):
        url, title = search_results.pop(0)
        parent_row = self.w.add_parent_row(searchterm, url, title)

        for search_result in search_results:
            url, title = search_result
            self.w.add_child_row(parent_row, searchterm, url, title)

    def _finish_search(self):
        self.w.statusBar().clearMessage()
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
