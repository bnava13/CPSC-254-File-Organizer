from PyQt5.QtWidgets import QTreeView, QFileSystemModel

class FolderView(QTreeView):
    def __init__(self, folder_selected_callback):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(""))
        self.setHeaderHidden(True)

        # Folder selection callback
        self.clicked.connect(lambda index: folder_selected_callback(self.model.filePath(index)))
