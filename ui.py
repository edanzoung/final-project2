from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QGridLayout, QLineEdit,
    QListWidget,QInputDialog, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from manager import StockManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Title
        self.setWindowTitle("Stock Manager")
        # Window Frame Size
        self.resize(800, 400)

        # Class StockManager
        self.manager = StockManager()

        # Grid Items list
        self.list_items_grid = QGridLayout()

        # Add New Item
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("New item name")
        btn_add = QPushButton("Add New Item")
        btn_add.clicked.connect(self.add_new_item)

        # Grid Items in Stock
        self.stock_grid = QGridLayout()

        # Grouping Widgets Vertically
        layout = QVBoxLayout()

        layout.addWidget(QLabel("List Items"))
        layout.addLayout(self.list_items_grid)

        layout.addWidget(self.name_input)
        layout.addWidget(btn_add)

        layout.addWidget(QLabel("In Stock"))
        layout.addLayout(self.stock_grid)

        self.setLayout(layout)

        self.update_all()

    # List Items
    def build_list_items_grid(self):
        for i, item in enumerate(self.manager.get_items()):
            name = item["name"]
            btn = QPushButton(name)

            qty = item["qty"]

            if int(qty) == 0:
                btn.clicked.connect(lambda _, n=item: self.manage_new_item(n))
            else:
                btn.clicked.connect(lambda _, n=item : self.manage_item_already_in_stock(n) )

            if item["image"]:
                img = item["image"]
                btn.setIcon(QIcon(img))
                btn.setIconSize(QSize(50, 50))


            self.list_items_grid.addWidget(btn, i // 4, i % 4)

    # Add New Item
    def add_new_item(self):
        name = self.name_input.text()
        if not name:
            return

        self.manager.add_new_item(name)
        self.name_input.clear()
        self.update_all()

    # Add Item in stock
    def add_item(self, name):
        qty, ok = QInputDialog.getInt(
            self,
            "Quantity",
            f"Enter quantity for {name}:",
            1,      # default
            1,      # min
            1000    # max
        )

        if ok:
            self.manager.add_item_in_stock(name, qty)
            self.update_all()

    # Update Stock List
    def update_stock(self):
        for i, item in enumerate(self.manager.get_items()):
            name = item["name"]
            qty = item["qty"]

            if int(qty) == 0:
                continue

            btn = QPushButton(name)
            btn.clicked.connect(lambda _, n=item : self.manage_stock(n))

            if item["image"]:
                img = item["image"]
                btn.setIcon(QIcon(img))
                btn.setIconSize(QSize(50, 50))

            # qty label
            qty_label = QLabel(str(qty), btn)
            qty_label.setStyleSheet("""
                background: black;
                color: white;
                border-radius: 10px;
                padding: 2px;
            """)
            qty_label.move(5, 5)

            self.stock_grid.addWidget(btn, i // 4, i % 4)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Update all Items
    def update_all(self):
        self.clear_layout(self.list_items_grid)
        self.clear_layout(self.stock_grid)

        self.build_list_items_grid()
        self.update_stock()

    # Manage new item
    def manage_new_item(self, item_widget):
        name = item_widget["name"]

        msg = QMessageBox(self)
        msg.setWindowTitle("Manage Item")
        msg.setText(name)

        btn_add_stock= msg.addButton("Add to stock", QMessageBox.ButtonRole.ActionRole)
        btn_img = msg.addButton("Update Image", QMessageBox.ButtonRole.ActionRole)
        btn_del = msg.addButton("Delete Item", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        #Add to stock
        if msg.clickedButton() == btn_add_stock:
            self.add_item(name)
            self.update_all()

        # UPDATE IMAGE
        elif msg.clickedButton() == btn_img:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", "", "Images (*.png *.jpg)"
            )
            if path:
                self.manager.update_image(name, path)
                self.update_all()

        # DELETE
        elif msg.clickedButton() == btn_del:
            self.manager.delete_item_by_name(name)
            self.update_all()

    # Manage item already in stock
    def manage_item_already_in_stock(self, item_widget):
        name = item_widget["name"]

        msg = QMessageBox(self)
        msg.setWindowTitle("Manage Item")
        msg.setText(name)
        
        btn_img = msg.addButton("Update Image", QMessageBox.ButtonRole.ActionRole)
        btn_del = msg.addButton("Delete Item", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        # UPDATE IMAGE
        if msg.clickedButton() == btn_img:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", "", "Images (*.png *.jpg)" 
            )
            if path:
                self.manager.update_image(name, path)
                self.update_all()

        # DELETE
        elif msg.clickedButton() == btn_del:
            self.manager.delete_item_by_name(name)
            self.update_all()

    #Manage Stock
    def manage_stock(self, item_widget):
        name = item_widget["name"]

        msg = QMessageBox(self)
        msg.setWindowTitle("Manage Item")
        msg.setText(name)
        
        btn_qty = msg.addButton("Update Value", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        #UPDATE QTY
        if msg.clickedButton() == btn_qty:
            current_qty = 0
            for item in self.manager.get_items():
                if item["name"] == name:
                    current_qty = int(item["qty"])

            new_qty, ok = QInputDialog.getInt(
                self,
                "Update Quantity",
                f"Set new quantity for {name}:",
                current_qty,
                0,
                10000
            )

            if ok:
                self.manager.update_qty(name, new_qty)
                self.update_all()