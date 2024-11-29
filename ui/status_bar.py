from PyQt5.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

    def update_status(self, message):
        self.showMessage(message)
