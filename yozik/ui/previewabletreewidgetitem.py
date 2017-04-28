from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt


class PreviewableTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, youtube_link, youtube_title, search_term, checked, parent=None):
        super().__init__(parent)

        self.setText(0, search_term)
        self.setText(1, youtube_title)
        self.setCheckState(2, checked)

        # There must be a better way how to make text look and behave like a link
        preview_link_brush = QBrush()
        preview_link_brush.setColor(QColor("#0000EE"))
        preview_link_font = QFont()
        preview_link_font.setUnderline(True)

        self.setForeground(1, preview_link_brush)
        self.setFont(1, preview_link_font)


        self.youtube_link = youtube_link

    def __hash__(self):
        return hash(self.youtube_link)

    def isChecked(self):
        if self.checkState(2) == Qt.Checked:
            return True
        return False

    def url(self):
        return self.youtube_link

    def title(self):
        return self.text(1)
