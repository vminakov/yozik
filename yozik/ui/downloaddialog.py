from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, \
    QProgressBar, QLineEdit, QLabel, QButtonGroup, QRadioButton, QComboBox, QFrame, QGroupBox

from yozik.core import Downloader


class DownloadDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = None
        self.downloadButton = None
        self.cancelButton = None
        self.finishButton = None
        self.openDestinationButton = None
        self.buttonLayout = None
        self.downloadToInputField = None
        self.downloadToBrowseButton = None

        self.buttonGroup = None
        self.audioRadio = None
        self.videoRadio = None
        self.formatCombobox = None

        self._audio_options = Downloader.AUDIO_FORMATS
        self._video_options = Downloader.VIDEO_FORMATS

        self.init_ui()

    def init_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._init_ui_top_frame())
        mainLayout.addWidget(self._init_ui_table())
        mainLayout.addLayout(self._init_ui_bottom_layout())

        self.setLayout(mainLayout)
        self.resize(800, 600)

    def _init_ui_top_frame(self):
        downloadToLabel = QLabel("Download to:")
        self.downloadToInputField = QLineEdit()
        self.downloadToInputField.setMinimumWidth(250)
        self.downloadToBrowseButton = QPushButton("Browse...")

        downloadToLayout = QHBoxLayout()
        downloadToLayout.addWidget(downloadToLabel)
        downloadToLayout.addWidget(self.downloadToInputField)
        downloadToLayout.addWidget(self.downloadToBrowseButton)
        downloadToLayout.addStretch()

        self.audioRadio = QRadioButton()
        self.audioRadio.setText("Download audio")
        self.audioRadio.setChecked(True)
        self.videoRadio = QRadioButton()
        self.videoRadio.setText("Download video")
        self.buttonGroup = QButtonGroup(parent=self)
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.audioRadio, 1)
        self.buttonGroup.addButton(self.videoRadio, 2)
        self.buttonGroup.buttonToggled.connect(self.format_toggled)

        downloadButtonsLayout = QVBoxLayout()
        downloadButtonsLayout.addWidget(self.audioRadio)
        downloadButtonsLayout.addWidget(self.videoRadio)

        downloadOptions = QGroupBox()
        downloadOptions.setTitle("Download options")
        downloadOptions.setLayout(downloadButtonsLayout)


        formatLabel = QLabel("Convert to:")
        self.formatCombobox = QComboBox()
        self.formatCombobox.addItems(self._audio_options)

        formatButtonsLayout = QVBoxLayout()
        formatButtonsLayout.addWidget(formatLabel)
        formatButtonsLayout.addWidget(self.formatCombobox)

        formatOptions = QGroupBox()
        formatOptions.setTitle("Postprocessing options")
        formatOptions.setLayout(formatButtonsLayout)

        optionsLayoutContainer = QHBoxLayout()
        optionsLayoutContainer.addWidget(downloadOptions)
        optionsLayoutContainer.addWidget(formatOptions)
        optionsLayoutContainer.addStretch()

        frameLayout = QVBoxLayout()
        frameLayout.addLayout(downloadToLayout)
        frameLayout.addLayout(optionsLayoutContainer)

        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setLayout(frameLayout)

        return frame

    def _init_ui_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Url", "Download Progress", "Postprocessing Progress"])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 160)
        self.table.setColumnWidth(3, 160)

        return self.table

    def _init_ui_bottom_layout(self):
        self.downloadButton = QPushButton("Download")
        self.cancelButton = QPushButton("Cancel")
        self.finishButton = QPushButton("Done")
        self.openDestinationButton = QPushButton("Open destination folder")

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.downloadButton)

        return self.buttonLayout

    def format_toggled(self, button, checked):
        if button == self.videoRadio:
            self.formatCombobox.clear()
            self.formatCombobox.addItems(self._video_options)
        if button == self.audioRadio:
            self.formatCombobox.clear()
            self.formatCombobox.addItems(self._audio_options)

    def add_table_row(self, title, url):
        downloadProgressWidget = QProgressBar()
        downloadProgressWidget.setMinimum(0)
        downloadProgressWidget.setMaximum(100)

        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        self.table.setItem(row_index, 0, QTableWidgetItem(title))
        self.table.setItem(row_index, 1, QTableWidgetItem(url))
        self.table.setCellWidget(row_index, 2, downloadProgressWidget)

    def show_postprocessor_progress(self, row_index):
        postprocessorProgressWidget = QProgressBar()
        postprocessorProgressWidget.setMinimum(0)
        postprocessorProgressWidget.setMaximum(0)

        self.table.setCellWidget(row_index, 3, postprocessorProgressWidget)

    def hide_postprocessor_progress(self, row_index):
        postprocessorProgressWidget = QProgressBar()
        postprocessorProgressWidget.setMinimum(0)
        postprocessorProgressWidget.setMaximum(100)
        postprocessorProgressWidget.setValue(100)

        self.table.setCellWidget(row_index, 3, postprocessorProgressWidget)

    def exchange_download_with_cancel(self):
        self.buttonLayout.removeWidget(self.downloadButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.downloadButton.hide()

    def exchange_cancel_with_finish(self):
        self.buttonLayout.removeWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.finishButton)
        self.cancelButton.hide()

        self.buttonLayout.addWidget(self.openDestinationButton)


