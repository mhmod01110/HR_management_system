import sys
import os

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from candidates_data_handler.interface import *
from APP_GUI.intro_page import *
from APP_GUI.candidate_page import *

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QPushButton, QFormLayout, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDialogButtonBox, QSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام إدارة المرشحين للوظائف")
        # self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #ffffff;")
        
        # Set the app icon
        self.icons_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))
        app_icon_path = os.path.join(self.icons_path, "app_icon.png")  # Make sure "app_icon.png" exists
        self.setWindowIcon(QIcon(app_icon_path))  # Set the icon

        # Main layout
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("نظام إدارة المرشحين للوظائف")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("background-color: #e1683a; color: white; padding: 15px;")
        main_layout.addWidget(header)

        # Content layout
        content_layout = QHBoxLayout()

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # Sidebar TreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #b06614;
                color: white;
                border: none;
            }
            QTreeWidget::item {
                padding: 12;
                font-size: 16px;
            }
            QTreeWidget::item:selected {
                background-color: #ec2b13;
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #e6c819;
            }
        """)
        self.tree_widget.currentItemChanged.connect(self.display_page)
        
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(sidebar_layout)
        self.sidebar_widget.setFixedWidth(200)  # Default sidebar width

        # Toggle button
        self.toggle_button = QPushButton("⮜")
        self.toggle_button.setFixedWidth(30)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #b06614;
                color: white;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e6c819;
            }
        """)
        # self.toggle_button.setSizePolicy(QPushButton.Minimum, QPushButton.Expanding)
        self.toggle_button.clicked.connect(self.toggle_sidebar)



        # Main area (StackedWidget)
        self.stacked_widget = QStackedWidget()

        # Intro Page (Login)
        self.intro_page = IntroPage()
        self.intro_page.login_successful.connect(self.enable_candidates_page)  # Connect login signal
        self.add_tree_item("صفحة الدخول", "emails.png", 0)
        self.stacked_widget.addWidget(self.intro_page)  # index 0
        # Automatically select the "Login Page" item
        login_item = self.tree_widget.topLevelItem(0)  # Assuming "Login Page" is the first item
        self.tree_widget.setCurrentItem(login_item)

        # Candidates Management Page
        self.candidates_page = CandidatesManagementPage()
        self.add_tree_item("صفحة المرشحين", "users.png", 1, enabled=False)
        self.stacked_widget.addWidget(self.candidates_page)  # index 1

        # Logout Tree Item
        self.add_tree_item("تسجيل الخروج", "logout.png", -1, enabled=False)  # Assuming "logout_icon.png" exists
        
        # Combine layouts
        content_layout.addLayout(sidebar_layout, 1)
        content_layout.addWidget(self.toggle_button)
        content_layout.addWidget(self.stacked_widget, 4)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.sidebar_visible = True

    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar."""
        if self.sidebar_visible:
            self.sidebar_widget.hide()
            self.toggle_button.setText("⮞")
        else:
            self.sidebar_widget.show()
            self.toggle_button.setText("⮜")
        self.sidebar_visible = not self.sidebar_visible
        
    def add_tree_item(self, text, icon_file, page_index, enabled=True):
        """Add an item to the sidebar."""
        item = QTreeWidgetItem()
        item.setText(0, text)
        icon_path = os.path.join(self.icons_path, icon_file)
        item.setIcon(0, QIcon(icon_path))
        item.setData(0, Qt.UserRole, page_index)
        item.setDisabled(not enabled)  # Disable item if not enabled
        item.setFont(0, QFont("Arial", 12))
        
        # # Special handling for logout item
        # if page_index == -1:  # Special logout item
        #     item.setBackground(0, QBrush(QColor("#7d0200")))  # Set background color        
        self.tree_widget.addTopLevelItem(item)


    def enable_candidates_page(self):
        self.tree_widget.topLevelItem(1).setDisabled(False)  # Enable "Candidates Page"
        self.tree_widget.topLevelItem(2).setDisabled(False)  # Enable "Logout"
        self.stacked_widget.setCurrentIndex(1)  # Switch to "Candidates Page"
        self.tree_widget.setCurrentItem(self.tree_widget.topLevelItem(1))  # Select "Candidates Page"
        self.tree_widget.topLevelItem(0).setDisabled(True)  # Disable "Login Page"

    def handle_logout(self):
        self.tree_widget.topLevelItem(0).setDisabled(False)  # Enable "Login Page"
        self.tree_widget.setCurrentItem(self.tree_widget.topLevelItem(0))  # Select "Login Page"
        self.stacked_widget.setCurrentIndex(0)  # Switch to "Login Page"
        self.tree_widget.topLevelItem(1).setDisabled(True)  # Disable "Candidates Page"
        self.tree_widget.topLevelItem(2).setDisabled(True)  # Disable "Logout"
        # Show a logout confirmation message
        QMessageBox.information(self, "تم تسجيل الخروج", "تم تسجيل الخروج من البرنامج.")
        # Re-enable "Login Page"
        


    def display_page(self, current, previous):
        """Switch pages."""
        if current:
            page_index = current.data(0, Qt.UserRole)
            if page_index == -1:  # If it's the Logout item
                self.handle_logout()
            else:
                self.stacked_widget.setCurrentIndex(page_index)

            if page_index == 1:  # Candidates Management page
                self.candidates_page.populate_candidate_table()  # Refresh candidates data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
