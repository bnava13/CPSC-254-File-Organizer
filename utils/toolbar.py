from PyQt5.QtWidgets import QHBoxLayout, QPushButton

class Toolbar:
    def __init__(self, sort_callback, toggle_callback):
        self.layout = QHBoxLayout()

        # Sorting Buttons
        self.sort_by_name_btn = QPushButton("Sort by Name")
        self.sort_by_size_btn = QPushButton("Sort by Size")
        self.sort_by_type_btn = QPushButton("Sort by Type")
        self.toggle_order_btn = QPushButton("Toggle Order")

        # Add to Layout
        self.layout.addWidget(self.sort_by_name_btn)
        self.layout.addWidget(self.sort_by_size_btn)
        self.layout.addWidget(self.sort_by_type_btn)
        self.layout.addWidget(self.toggle_order_btn)

        # Connect Buttons
       
        # 0: Name
        self.sort_by_name_btn.clicked.connect(lambda: sort_callback(0))
        
        # 1: Size
        self.sort_by_size_btn.clicked.connect(lambda: sort_callback(1))
        
        # 2:Type
        self.sort_by_type_btn.clicked.connect(lambda: sort_callback(2))
       
        self.toggle_order_btn.clicked.connect(toggle_callback)
