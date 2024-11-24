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
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

class IntroPage(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("مرحباً بكم في برنامج إدارة المرشحين للوظائف")
        self.setStyleSheet("background-color: #ffffff;")
        self.icons_path = (
            os.path.join(sys._MEIPASS, "icons")  # When running as a bundled app
            if getattr(sys, "frozen", False)
            else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))  # During development
        )


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
            logo_label.setPixmap(QPixmap(logo_path).scaled(500, 500, Qt.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignCenter)
        else:
            logo_label.setText("Logo Here")
            logo_label.setStyleSheet("color: #333; font-size: 18px;")

        # Login form layout
        login_layout = QVBoxLayout()
        login_layout.setSpacing(15)

        username_label = QLabel("اسم المستخدم:")
        username_label.setFont(QFont("Arial", 12))
        username_label.setStyleSheet("background-color: #ffffff;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("ادخل اسم المستخدم")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 10px;")
        self.username_input.returnPressed.connect(self.handle_login)

        password_label = QLabel("كلمة المرور:")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("background-color: #ffffff;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("ادخل كلمة المرور")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 10px;")
        self.password_input.returnPressed.connect(self.handle_login)

        # Interactive image button
        self.image_button = QLabel()
        button_img = "login.png"  # Replace with your image file
        button_path = os.path.join(self.icons_path, button_img)

        if os.path.exists(button_path):
            self.image_button.setPixmap(QPixmap(button_path).scaled(100, 100, Qt.KeepAspectRatio))
        else:
            self.image_button.setText("Login Button")
            self.image_button.setAlignment(Qt.AlignCenter)

        self.image_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.image_button.setAlignment(Qt.AlignCenter)

        # Style for hover effect
        self.image_button.setStyleSheet("""
            QLabel {
                background-color: none;
            }
            QLabel:hover {
                transform: scale(1.1);
                border: 2px solid #007BFF;
                border-radius: 20px;
            }
        """)

        # Connect the click event
        self.image_button.mousePressEvent = self.handle_login

        # Add widgets to the login form
        login_layout.addWidget(username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(self.image_button)

        # Add logo and form to the main layout
        layout.addWidget(logo_label)
        layout.addLayout(login_layout)

        return layout

    def handle_login(self, event=None):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":  # Replace with actual validation
            QMessageBox.information(self, "تم تسجيل الدخول بنجاح", "مرحبا بكم !")
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "خطأ في تسجيل الدخول", "من فضلك تحقق من اسم المستخدم و كلمة المرور")
