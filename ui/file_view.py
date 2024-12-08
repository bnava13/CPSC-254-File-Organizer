from PyQt5.QtWidgets import QTableView, QFileSystemModel, QMessageBox
from PyQt5.QtCore import QSortFilterProxyModel, Qt
import os
import shutil

class FileProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.search_text = ""

    def set_search_text(self, text):
        self.search_text = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.search_text:
            return True
            
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        filename = source_model.fileName(index).lower()
        
        return self.search_text in filename

class FileView(QTableView):
    def __init__(self):
        super().__init__()
        self.file_system_model = QFileSystemModel()
        self.proxy_model = FileProxyModel()
        self.proxy_model.setSourceModel(self.file_system_model)
        self.model = QFileSystemModel()
        self.setModel(self.model)
        # Enable multiple selection
        self.setSelectionMode(QTableView.ExtendedSelection)
        # Show selection by rows
        self.setSelectionBehavior(QTableView.SelectRows)

    def set_folder_path(self, folder_path):
        self.setRootIndex(self.model.setRootPath(folder_path))

    def search_files(self, text):
        self.proxy_model.set_search_text(text)

    def sort_files(self, column, order):
        self.sortByColumn(column, order)

    def delete_selected_files(self):
        # Get selected indexes
        selected_rows = self.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "No files selected for deletion")
            return 0

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {len(selected_rows)} selected items?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            deleted_count = 0
            errors = []

            for index in selected_rows:
                file_path = self.model.filePath(index)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"Error deleting {file_path}: {str(e)}")

            # Show results
            if errors:
                QMessageBox.warning(
                    self,
                    "Delete Results",
                    f"Deleted {deleted_count} items\nErrors occurred:\n" + "\n".join(errors)
                )
            elif deleted_count > 0:
                QMessageBox.information(
                    self,
                    "Delete Success",
                    f"Successfully deleted {deleted_count} items"
                )

            return deleted_count
        return 0
