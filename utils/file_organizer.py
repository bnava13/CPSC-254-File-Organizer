from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget
from PyQt5.QtCore import Qt
from ui.folder_view import FolderView
from ui.file_view import FileView
from utils.toolbar import Toolbar
from ui.status_bar import StatusBar

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 1000, 600)

        # Sorting order
        self.sort_order = Qt.AscendingOrder

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Splitter for Tree View and File View
        splitter = QSplitter(Qt.Horizontal)
        self.folder_view = FolderView(self.folder_selected)
        self.file_view = EnhancedFileView()
        splitter.addWidget(self.folder_view)
        splitter.addWidget(self.file_view)

        # Layout for Central Widget
        layout = QVBoxLayout(central_widget)
        layout.addWidget(splitter)

        # Toolbar
        self.toolbar = Toolbar(self.sort_files, self.toggle_sort_order, self.delete_selected_files, self.search_callback=self.search_files)
        layout.addLayout(self.toolbar.layout)

        # Status Bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def folder_selected(self, folder_path):
        self.file_view.set_folder_path(folder_path)
        self.status_bar.update_status(f"Current Folder: {folder_path}")

    def sort_files(self, column):
        self.file_view.sort_files(column, self.sort_order)
        column_name = ["Name", "Size", "Type"][column]
        order = "Ascending" if self.sort_order == Qt.AscendingOrder else "Descending"
        self.status_bar.update_status(f"Sorted by {column_name} ({order})")

    def toggle_sort_order(self):
        self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        order = "Ascending" if self.sort_order == Qt.AscendingOrder else "Descending"
        self.status_bar.update_status(f"Sorting order changed to {order}")

    def search_files(self, search_text):
        self.file_view.search_files(search_text)
        self.status_bar.update_status(f"Searching for: {search_text}")

    def delete_selected_files(self):
        deleted_count = self.file_view.delete_selected_files()
        if deleted_count:
            self.status_bar.update_status(f"Deleted {deleted_count} items")
