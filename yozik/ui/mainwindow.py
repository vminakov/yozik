from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, \
    QPlainTextEdit, QGroupBox, QLabel, QAction, qApp, \
    QDialog, QTreeWidget

from yozik.ui import PreviewableTreeWidgetItem
import yozik.resources

if float(QT_VERSION_STR[:3]) > 5.5:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
else:
    from PyQt5.QtWebKitWidgets import QWebView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.clearButton = None
        self.findButton = None
        self.inputField = None
        self.downloadButton = None
        self.treeView = None

        self.init_ui()
        self.setWindowTitle("Yozik")
        self.setWindowIcon(QIcon(":/resources/yozik.png"))

        self.link_map = {}
        self.loading_spinner = None


    def init_ui(self):
        self.statusBar()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._init_ui_search_box())
        mainLayout.addWidget(self._init_ui_download_box())
        mainLayout.setStretch(1, 5)
        self._init_ui_menu()

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        self.resize(800, 600)

    def _init_ui_search_box(self):
        self.clearButton = QPushButton("Clear")
        self.findButton = QPushButton("Find")

        inputButtonContainer = QVBoxLayout()
        inputButtonContainer.addWidget(self.clearButton)
        inputButtonContainer.addStretch()
        inputButtonContainer.addWidget(self.findButton)

        self.inputField = QPlainTextEdit()
        self.inputField.setPlaceholderText("Enter search terms, youtube links or full playlists separated by new lines")

        inputGroupLayout = QHBoxLayout()
        inputGroupLayout.addWidget(self.inputField)
        inputGroupLayout.addLayout(inputButtonContainer)

        inputGroupContainer = QGroupBox()
        inputGroupContainer.setTitle("Find")
        inputGroupContainer.setLayout(inputGroupLayout)

        return inputGroupContainer

    def _init_ui_download_box(self):
        self.downloadButton = QPushButton("Download")

        downloadToLayout = QHBoxLayout()
        downloadToLayout.addStretch()
        downloadToLayout.addWidget(self.downloadButton)

        self.treeView = QTreeWidget()
        self.treeView.setColumnCount(3)
        self.treeView.setHeaderLabels(["Search term", "Youtube page", "Download?"])
        self.treeView.itemClicked.connect(self._show_preview_dialog)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.setColumnWidth(1, 450)
        self.treeView.setColumnWidth(2, 60)

        downloadGroupLayout = QVBoxLayout()
        downloadGroupLayout.addWidget(self.treeView)
        downloadGroupLayout.addLayout(downloadToLayout)

        downloadGroupContainer = QGroupBox()
        downloadGroupContainer.setTitle("Preview")
        downloadGroupContainer.setLayout(downloadGroupLayout)

        return downloadGroupContainer

    def _init_ui_menu(self):
        exitAction = QAction("Quit", self)
        exitAction.triggered.connect(qApp.quit)

        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self._show_about_dialog)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        fileMenu.addAction(exitAction)

        aboutMenu = bar.addMenu("About")
        aboutMenu.addAction(aboutAction)

    def add_parent_row(self, search_term, youtube_link, youtube_title):
        item = PreviewableTreeWidgetItem(
            youtube_link=youtube_link,
            youtube_title=youtube_title,
            search_term=search_term,
            checked=Qt.Checked
        )
        self.treeView.insertTopLevelItem(self.treeView.topLevelItemCount(), item)
        self.link_map[item] = item
        return item

    def add_child_row(self, parent, search_term, youtube_link, youtube_title):
        item = PreviewableTreeWidgetItem(
            youtube_link=youtube_link,
            youtube_title=youtube_title,
            search_term="",
            checked=Qt.Unchecked
        )
        parent.addChild(item)

        self.link_map[item] = item

    def _show_about_dialog(self):
        logoLabel = QLabel()
        logoLabel.setPixmap(QPixmap(":/resources/yozik.png"))

        logoLayout = QHBoxLayout()
        logoLayout.addStretch()
        logoLayout.addWidget(logoLabel)
        logoLayout.addStretch()

        titleLayout = QHBoxLayout()
        titleLayout.addStretch()
        titleLayout.addWidget(QLabel("<b>Yozik - The Youtube ripper</b>"))
        titleLayout.addStretch()

        versionLayout =QHBoxLayout()
        versionLayout.addStretch()
        versionLayout.addWidget(QLabel("Version: 0.0.1"))
        versionLayout.addStretch()

        dialogLayout = QVBoxLayout()
        dialogLayout.addLayout(logoLayout)
        dialogLayout.addLayout(titleLayout)
        dialogLayout.addLayout(versionLayout)

        d = QDialog(self)
        d.setLayout(dialogLayout)
        d.exec_()

    def _show_preview_dialog(self, item, column):
        if column == 1:
            url = self.link_map[item].url()
            webviewLayout = QVBoxLayout()
            w = QWebView()
            w.load(QUrl(url))
            webviewLayout.addWidget(w)

            d = QDialog(self)
            d.setLayout(webviewLayout)
            d.exec_()

    def toggle_loading_spinner(self):
        if self.loading_spinner is None:
            x = self.treeView.width() / 2 - 40
            y = self.treeView.height() / 2

            movie = QMovie(":/resources/spinner.gif")
            movie.setScaledSize(QSize(40, 40))

            self.loading_spinner = QLabel("", self.treeView)
            self.loading_spinner.setGeometry(x, y, 40, 40)
            self.loading_spinner.setMovie(movie)
            movie.start()
            self.loading_spinner.show()
        else:
            self.loading_spinner.hide()
            self.loading_spinner = None

    def toggle_event_processing(self):
        """ todo: disabla event handling in the tree view while search is in progress"""
        pass
