from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, qApp
from PyQt5.QtCore import QProcess

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
        self.downloadButton = QPushButton("Download")
        self.cancelButton = QPushButton("Cancel")

        self.downloadButton.clicked.connect(self.restart_app)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.downloadButton)
        return buttonLayout

    def restart_app(self):
        proc = QProcess()
        import os
        import sys
        proc.startDetached(os.path.abspath(__file__))

        qApp.exit()
