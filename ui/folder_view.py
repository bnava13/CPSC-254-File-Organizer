from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt, QDir 

class FolderView(QTreeView):
    def __init__(self, folder_selected_callback):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(""))
        self.setHeaderHidden(True)

         # Hide all columns except the name column
        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)
            
        # Only show directories - using QDir.Filter instead of Qt
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)

        # Folder selection callback
        self.clicked.connect(lambda index: folder_selected_callback(self.model.filePath(index)))
