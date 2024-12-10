from PyQt5.QtWidgets import QTableView, QFileSystemModel, QMessageBox
from PyQt5.QtCore import Qt, QDir, QTimer
import os
import shutil

class FileView(QTableView):
    def __init__(self):
        super().__init__()

        # Initialize file system model
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # Set the model
        self.setModel(self.model)

        # Selection settings
        self.setSelectionMode(QTableView.ExtendedSelection)
        self.setSelectionBehavior(QTableView.SelectRows)

        # Show all columns
        for i in range(self.model.columnCount()):
            self.setColumnHidden(i, False)

        # Track current folder, search text, and real-time search state
        self.current_folder = None
        self.current_search = ""
        self.all_files = []
        self.is_searching = False  # Add a flag to track if a search is in progress
        self.no_results_shown = False  # Flag to track if "no results" message has been shown

        # Timer for real-time search
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(300)  # Wait 300ms after typing before filtering
        self.search_timer.timeout.connect(self.apply_search_filter)

        # Global search flag
        self.is_global_search = False  # Flag to indicate if it's a global search

    def set_folder_path(self, folder_path):
        """Set the root folder and refresh the table based on search"""
        if folder_path and os.path.exists(folder_path):
            self.current_folder = folder_path
            self.model.setRootPath(folder_path)
            self.setRootIndex(self.model.index(folder_path))
            if not self.is_searching:
                self.apply_search_filter()
        else:
            # Handle the case where the folder path is invalid or None
            self.current_folder = None
            QMessageBox.warning(self, "Invalid Folder", "The specified folder path is invalid or does not exist.")

    def search_files(self, text, global_search=False):
        """Perform real-time global search across all directories"""
        self.is_searching = True  # Indicate search is in progress
        self.current_search = text.lower().strip()
        self.is_global_search = global_search

        if not self.current_search:
            # If search is empty, reset to show all files in current folder
            self.set_folder_path(self.current_folder)
            self.all_files = []
            self.apply_search_filter()
            self.is_searching = False  # End search
            return

        # If it's a global search, collect all files from the entire file system
        if self.is_global_search:
            self.all_files = self.collect_files(QDir.rootPath())  # Or specify a home directory, e.g., QDir.homePath()
        elif self.current_folder:
            self.all_files = self.collect_files(self.current_folder)
        else:
            QMessageBox.warning(self, "No Folder Set", "Please set a valid folder before searching.")
            self.is_searching = False  # End search
            return

        # Start the search filter after typing is done (real-time update)
        self.search_timer.start()

    def collect_files(self, root_folder):
        """Collect all file paths and names in the root folder and subfolders"""
        all_files = []
        if not root_folder:
            return all_files  # Return empty if no root folder

        for root, dirs, files in os.walk(root_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                all_files.append(file_path)
        return all_files

    def apply_search_filter(self):
        """Apply the search filter on all files"""
        if not self.current_search:
            self.is_searching = False  # End search
            return

        # Hide all rows initially
        total_rows = self.model.rowCount(self.rootIndex())
        found_results = False  # Flag to check if any match was found

        # Filter the rows based on the current search across all files
        for row in range(total_rows):
            index = self.model.index(row, 0, self.rootIndex())

            if index.isValid():
                file_name = self.model.fileName(index)
                file_path = self.model.filePath(index)

                # Match the file name with the search term
                matched = any(self.current_search in file.lower() for file in self.all_files if file_path == file)

                if matched:
                    self.setRowHidden(row, False)
                    found_results = True
                else:
                    self.setRowHidden(row, True)

        # If no results were found, show a message
        if not found_results and not self.no_results_shown:
            self.no_results_shown = True
            QMessageBox.warning(self, "No Results", "No files found matching the search term")

        # Reset the flag if any results were found
        if found_results:
            self.no_results_shown = False

        self.is_searching = False  # End search

    def reset_search(self):
        """Reset search and show all files in current folder"""
        self.current_search = ""
        self.is_global_search = False
        self.set_folder_path(self.current_folder)  # Restore folder view
        self.apply_search_filter()  # Show all files in the folder

    def sort_files(self, column, order):
        """Sort files by a specified column and order"""
        self.sortByColumn(column, order)

    def delete_selected_files(self):
        """Delete selected files and folders"""
        selected_rows = self.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Warning", "No files selected for deletion")
            return 0

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

            # Refresh the view while maintaining the search
            self.apply_search_filter()

            return deleted_count
        return 0
