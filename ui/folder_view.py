from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt, QDir 

class FolderView(QTreeView):
    def __init__(self, folder_selected_callback):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.homePath()))
        self.setHeaderHidden(True)

         # Hide all columns except the name column
        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)

        # Folder selection callback
        self.clicked.connect(lambda index: folder_selected_callback(self.model.filePath(index)))
