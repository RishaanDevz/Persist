import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QListWidget, QListWidgetItem, QLineEdit, QLabel, QMessageBox)
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QFont

class ObjectiveItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(Qt.Unchecked)

class NotesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.custom_font = QFont("SF Pro, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif", 12)
        
        self.setWindowTitle('Persist')
        self.setGeometry(300, 300, 350, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QLineEdit, QListWidget {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FF4D06;
                border: none;
                color: #FFFFFF;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FF6A33;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #333333;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Persist")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont(self.custom_font.family(), 24))
        title_label.setStyleSheet("margin: 10px 0;")
        layout.addWidget(title_label)
        
        # Input area
        input_layout = QHBoxLayout()
        self.objective_input = QLineEdit(self)
        self.objective_input.setPlaceholderText("Enter a task...")
        self.objective_input.setFont(self.custom_font)
        self.objective_input.returnPressed.connect(self.add_objective)
        add_button = QPushButton("+")
        add_button.setFont(self.custom_font)
        add_button.clicked.connect(self.add_objective)
        add_button.setFixedSize(40, 40)
        input_layout.addWidget(self.objective_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)
        
        # Objectives list
        self.objectives_list = QListWidget(self)
        self.objectives_list.setFont(self.custom_font)
        self.objectives_list.itemClicked.connect(self.toggle_objective)
        layout.addWidget(self.objectives_list)
        
        # Done button
        self.done_btn = QPushButton("Mark All as Done")
        self.done_btn.setFont(self.custom_font)
        self.done_btn.clicked.connect(self.mark_all_done)
        layout.addWidget(self.done_btn)
        
        self.setLayout(layout)
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
        
    def add_objective(self):
        text = self.objective_input.text().strip()
        if text:
            item = ObjectiveItem(text)
            item.setFont(self.custom_font)
            self.objectives_list.addItem(item)
            self.objective_input.clear()
        
    def toggle_objective(self, item):
        self.set_item_checked(item, item.checkState() != Qt.Checked)
        self.check_all_done()
        
    def set_item_checked(self, item, checked):
        font = item.font()
        if checked:
            font.setStrikeOut(True)
            item.setCheckState(Qt.Checked)
            item.setForeground(Qt.gray)
        else:
            font.setStrikeOut(False)
            item.setCheckState(Qt.Unchecked)
            item.setForeground(Qt.white)
        item.setFont(font)
        
    def mark_all_done(self):
        for i in range(self.objectives_list.count()):
            item = self.objectives_list.item(i)
            self.set_item_checked(item, True)
        self.check_all_done()
        
    def check_all_done(self):
        all_done = all(self.objectives_list.item(i).checkState() == Qt.Checked 
                       for i in range(self.objectives_list.count()))
        if all_done and self.objectives_list.count() > 0:
            self.show_completion_message()
        
    def show_completion_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Congratulations!")
        msg_box.setText("All tasks completed! Great job!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1A1A1A;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FF4D06;
                color: #FFFFFF;
                padding: 5px 15px;
                border-radius: 3px;
            }
        """)
        msg_box.exec()
        
        # Close the application after showing the message
        QTimer.singleShot(1000, self.close_application)
        
    def close_application(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notes_window = NotesWindow()
    notes_window.show()
    sys.exit(app.exec())