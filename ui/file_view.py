from PyQt5.QtWidgets import (QTableView, QFileSystemModel, QLineEdit, 
                          QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
import os
import shutil

class SearchProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.search_text = ""

    def set_search_text(self, text):
        self.search_text = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        
        # Get file/folder name
        name = source_model.fileName(index).lower()
        return self.search_text in name

class EnhancedFileView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.search_files)
        layout.addWidget(self.search_bar)

        # File view
        self.file_system_model = QFileSystemModel()
        self.proxy_model = SearchProxyModel()
        self.proxy_model.setSourceModel(self.file_system_model)
        
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSelectionMode(QTableView.ExtendedSelection)
        layout.addWidget(self.table_view)

    def set_folder_path(self, folder_path):
        self.file_system_model.setRootPath(folder_path)
        self.table_view.setRootIndex(
            self.proxy_model.mapFromSource(
                self.file_system_model.index(folder_path)
            )
        )

    def search_files(self, text):
        self.proxy_model.set_search_text(text)

    def sort_files(self, column, order):
        self.table_view.sortByColumn(column, order)

    def get_selected_files(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        return [
            self.file_system_model.filePath(
                self.proxy_model.mapToSource(index)
            )
            for index in selected_indexes
        ]

    def delete_selected_files(self):
        selected_files = self.get_selected_files()
        
        if not selected_files:
            QMessageBox.warning(self, "Warning", "No files selected")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {len(selected_files)} selected items?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            errors = []
            deleted_count = 0

            for file_path in selected_files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    else:
                        shutil.rmtree(file_path)
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"Error deleting {file_path}: {str(e)}")

            if errors:
                QMessageBox.warning(
                    self,
                    "Delete Results",
                    f"Deleted {deleted_count} items.\nErrors occurred:\n" + 
                    "\n".join(errors)
                )
            return deleted_count
