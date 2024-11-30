from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLineEdit, QFileDialog, QListWidget,
                           QLabel, QMessageBox)
from PyQt5.QtCore import Qt
import os
import shutil

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create directory selection widgets
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select directory to organize")
        dir_button = QPushButton("Browse")
        dir_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        layout.addLayout(dir_layout)
        
        # Create search widgets
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.textChanged.connect(self.search_files)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Create file list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.file_list)
        
        # Create buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected)
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_files)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        
        # Initialize variables
        self.current_directory = None
        self.all_files = []

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.current_directory = directory
            self.dir_input.setText(directory)
            self.refresh_files()

    def refresh_files(self):
        if not self.current_directory:
            return
            
        self.all_files = []
        self.file_list.clear()
        
        try:
            for root, _, files in os.walk(self.current_directory):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.current_directory)
                    self.all_files.append((rel_path, full_path))
                    self.file_list.addItem(rel_path)
            
            self.status_label.setText(f"Found {len(self.all_files)} files")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error refreshing files: {str(e)}")

    def search_files(self):
        search_text = self.search_input.text().lower()
        self.file_list.clear()
        
        if not search_text:
            # If search is empty, show all files
            for rel_path, _ in self.all_files:
                self.file_list.addItem(rel_path)
        else:
            # Show only matching files
            for rel_path, _ in self.all_files:
                if search_text in rel_path.lower():
                    self.file_list.addItem(rel_path)

    def delete_selected(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No files selected")
            return
            
        reply = QMessageBox.question(self, "Confirm Delete",
                                   f"Are you sure you want to delete {len(selected_items)} selected files?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            deleted_count = 0
            errors = []
            
            for item in selected_items:
                file_rel_path = item.text()
                # Find the full path from our stored files
                file_full_path = next(full_path for rel_path, full_path in self.all_files if rel_path == file_rel_path)
                
                try:
                    if os.path.exists(file_full_path):
                        if os.path.isfile(file_full_path):
                            os.remove(file_full_path)
                        else:
                            shutil.rmtree(file_full_path)
                        deleted_count += 1
                except Exception as e:
                    errors.append(f"Error deleting {file_rel_path}: {str(e)}")
            
            # Refresh the file list
            self.refresh_files()
            
            # Show results
            if errors:
                QMessageBox.warning(self, "Delete Results",
                                  f"Deleted {deleted_count} files.\nErrors occurred:\n" + "\n".join(errors))
            else:
                self.status_label.setText(f"Successfully deleted {deleted_count} files")