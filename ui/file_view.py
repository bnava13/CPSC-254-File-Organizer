from PyQt5.QtWidgets import QTableView, QFileSystemModel

class FileView(QTableView):
    def __init__(self):
        super().__init__()
        self.model = QFileSystemModel()
        self.setModel(self.model)

    def set_folder_path(self, folder_path):
        self.setRootIndex(self.model.setRootPath(folder_path))

    def sort_files(self, column, order):
        self.sortByColumn(column, order)
