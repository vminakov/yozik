from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt


class PreviewableTreeWidgetItem(QTreeWidgetItem):

    TREEVIEW_COLUMN_SEARCHTERM = 0
    TREEVIEW_COLUMN_LINK = 1
    TREEVIEW_COLUMN_CHECKBOX = 2

    def __init__(self, youtube_link, youtube_title, search_term, checked, parent=None):
        super().__init__(parent)

        self.setText(self.TREEVIEW_COLUMN_SEARCHTERM, search_term)
        self.setText(self.TREEVIEW_COLUMN_LINK, youtube_title)
        self.setCheckState(self.TREEVIEW_COLUMN_CHECKBOX, checked)

        # There must be a better way how to make text look and behave like a link
        preview_link_brush = QBrush()
        preview_link_brush.setColor(QColor("#0000EE"))
        preview_link_font = QFont()
        preview_link_font.setUnderline(True)

        self.setForeground(self.TREEVIEW_COLUMN_LINK, preview_link_brush)
        self.setFont(self.TREEVIEW_COLUMN_LINK, preview_link_font)


        self.youtube_link = youtube_link

    def __hash__(self):
        return hash(self.youtube_link)

    def isChecked(self):
        if self.checkState(self.TREEVIEW_COLUMN_CHECKBOX) == Qt.Checked:
            return True
        return False

    def url(self):
        return self.youtube_link

    def title(self):
        return self.text(1)
