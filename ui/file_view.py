# ui/file_view.py
from PyQt5.QtWidgets import QTableView, QFileSystemModel, QMessageBox
from PyQt5.QtCore import QSortFilterProxyModel, Qt
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
        name = source_model.fileName(index).lower()
        return self.search_text in name

class FileView(QTableView):
    def __init__(self):
        super().__init__()
        self.file_system_model = QFileSystemModel()
        self.proxy_model = SearchProxyModel()
        self.proxy_model.setSourceModel(self.file_system_model)
        self.setModel(self.proxy_model)
        self.setSelectionMode(QTableView.ExtendedSelection)
        
    def set_folder_path(self, folder_path):
        self.file_system_model.setRootPath(folder_path)
        self.setRootIndex(
            self.proxy_model.mapFromSource(
                self.file_system_model.index(folder_path)
            )
        )
        
    def search_files(self, text):
        self.proxy_model.set_search_text(text)
        
    def sort_files(self, column, order):
        self.sortByColumn(column, order)
        
    def get_selected_files(self):
        selected_indexes = self.selectionModel().selectedRows()
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
            return 0
            
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
        return 0


# ui/folder_view.py
from PyQt5.QtWidgets import QTreeView, QFileSystemModel

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
            
        # Only show directories
        self.model.setFilter(self.model.filter() | Qt.DirectoryOnly)
        
        # Folder selection callback
        self.clicked.connect(
            lambda index: folder_selected_callback(self.model.filePath(index))
        )


# ui/status_bar.py
from PyQt5.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        
    def update_status(self, message):
        self.showMessage(message)