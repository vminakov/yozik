from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, qApp

class InitialSetupDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloadButton = QPushButton("Download and install")
        self.cancelButton = QPushButton("Cancel")
        self.finishButton = QPushButton("Finish")
        self.continueButton = QPushButton("Continue")

        self.finishText = QLabel("Installed successfully. Restart Yozik to start using updated versions.")
        self.messageText = QLabel()

        self.table = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._init_ui_message())
        layout.addWidget(self._init_ui_table())
        layout.addLayout(self._init_ui_buttons())
        self.setLayout(layout)

        self.init_ui_buttons_layout_continue()

    def _init_ui_message(self):
        return self.messageText

    def _init_ui_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Program", "Current version", "Latest version"])

        return self.table

    def _init_ui_buttons(self):
        return QHBoxLayout()

    def init_ui_buttons_layout_missing(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.downloadButton)
        self._exchange_button_layout(buttonLayout)

    def init_ui_buttons_layout_upgradable(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.downloadButton)
        self._exchange_button_layout(buttonLayout)

    def init_ui_buttons_layout_finished(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.finishText)
        buttonLayout.addWidget(self.finishButton)
        self._exchange_button_layout(buttonLayout)

    def init_ui_buttons_layout_continue(self):
        self.messageText.setText("Everything is already up-to-date. Nothing to upgrade.")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.continueButton)
        self._exchange_button_layout(buttonLayout)

    def add_row(self, name=None, installed_version=None, available_version=None):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        self.table.setItem(row_index, 0, QTableWidgetItem(name))
        self.table.setItem(row_index, 1, QTableWidgetItem(installed_version))
        self.table.setItem(row_index, 2, QTableWidgetItem(available_version))

    def _exchange_button_layout(self, newLayout):
        self.layout().removeItem(self.layout().itemAt(2))
        self.layout().insertLayout(2, newLayout)
