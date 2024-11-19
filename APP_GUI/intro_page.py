import sys
import os

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from users_orders_manager
from candidates_data_handler.interface import *

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QPushButton, QFormLayout, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDialogButtonBox, QSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

class IntroPage(QWidget):
    login_successful = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to HR-Candidates Management System")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f0f0f0;")  # Light background color
        self.icons_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Create content layout
        self.content_layout = self.create_layout()

        # Add content to the center of the page
        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

    def create_layout(self):
        # Main vertical layout for logo and login box
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo_label = QLabel()
        logo_img = "logo.jpg"
        logo_path = os.path.join(self.icons_path, logo_img)

        if os.path.exists(logo_path):
            logo_label.setPixmap(QIcon(logo_path).pixmap(300, 300))  # Adjust size as needed
        else:
            logo_label.setText("Logo Here")  # Placeholder if the logo doesn't exist
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("color: #999; font-size: 18px;")

        # Login form layout
        login_layout = QVBoxLayout()
        login_layout.setSpacing(15)

        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Arial", 10))
        self.username_input.setStyleSheet("background-color: white;")

        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFont(QFont("Arial", 10))
        self.password_input.setStyleSheet("background-color: white;")


        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 12, QFont.Bold))
        login_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px; padding: 5px;")
        login_button.clicked.connect(self.handle_login)

        # Add widgets to the login form
        login_layout.addWidget(username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button)

        # Add logo and form to the main layout
        layout.addWidget(logo_label)
        layout.addLayout(login_layout)

        return layout

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":  # Replace with actual validation
            QMessageBox.information(self, "Login Successful", "Welcome!")
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
