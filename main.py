import sys
from PyQt5.QtWidgets import QApplication
from utils.file_organizer import FileOrganizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    organizer = FileOrganizer()
    organizer.show()
    sys.exit(app.exec())
