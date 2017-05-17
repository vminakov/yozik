from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, qApp
from PyQt5.QtCore import QProcess
from yozik.core import YoutubeDl

class InitialSetupDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.downloadButton = None
        self.cancelButton = None
        self.messageText = None
        self.table = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._init_ui_message())
        layout.addWidget(self._init_ui_table())
        layout.addLayout(self._init_ui_buttons())
        self.setLayout(layout)

    def _init_ui_message(self):
        text = QLabel("In order to start using Yozik you need to have following programs installed."
                      " Download and install them now?")
        return text

    def _init_ui_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Program", "Current version", "Latest version", "Download progress"])

        return self.table

    def _init_ui_buttons(self):
        self.downloadButton = QPushButton("Download and install")
        self.cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.downloadButton)
        return buttonLayout

    def add_row(self, name=None, installed_version=None, available_version=None):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        self.table.setItem(row_index, 0, QTableWidgetItem(name))
        self.table.setItem(row_index, 1, QTableWidgetItem(installed_version))
        self.table.setItem(row_index, 2, QTableWidgetItem(available_version))

