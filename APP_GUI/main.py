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
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR - Candidates Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #ecf0f1;")
        
        # Set the app icon
        self.icons_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))
        app_icon_path = os.path.join(self.icons_path, "app_icon.png")  # Make sure "app_icon.png" exists
        self.setWindowIcon(QIcon(app_icon_path))  # Set the icon

        # Main layout
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("HR - Candidates Management System")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("background-color: #34495e; color: white; padding: 20px;")
        main_layout.addWidget(header)

        # Content layout
        content_layout = QHBoxLayout()

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar TreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #2c3e50;
                color: white;
                border: none;
            }
            QTreeWidget::item {
                padding: 8px;
                font-size: 16px;
            }
            QTreeWidget::item:selected {
                background-color: #16a085;
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #44d6db;
            }
        """)
        self.tree_widget.currentItemChanged.connect(self.display_page)
        sidebar_layout.addWidget(self.tree_widget)

        # Main area (StackedWidget)
        self.stacked_widget = QStackedWidget()

        # Intro Page (Login)
        self.intro_page = IntroPage()
        self.intro_page.login_successful.connect(self.enable_candidates_page)  # Connect login signal
        self.add_tree_item("Login Page", "emails.png", 0)
        self.stacked_widget.addWidget(self.intro_page)  # index 0

        # Candidates Management Page
        self.candidates_page = CandidatesManagementPage()
        self.add_tree_item("Candidates", "users.png", 1, enabled=False)
        self.stacked_widget.addWidget(self.candidates_page)  # index 1

        # Logout Tree Item
        self.add_tree_item("Logout", "logout.png", -1)  # Assuming "logout_icon.png" exists
        
        # Combine layouts
        content_layout.addLayout(sidebar_layout, 1)
        content_layout.addWidget(self.stacked_widget, 4)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def add_tree_item(self, text, icon_file, page_index, enabled=True):
        """Add an item to the sidebar."""
        item = QTreeWidgetItem()
        item.setText(0, text)
        icon_path = os.path.join(self.icons_path, icon_file)
        item.setIcon(0, QIcon(icon_path))
        item.setData(0, Qt.UserRole, page_index)
        item.setDisabled(not enabled)  # Disable item if not enabled
        item.setFont(0, QFont("Arial", 12))
        
        # Special handling for logout item
        if page_index == -1:  # Special logout item
            item.setBackground(0, QBrush(QColor("#e74c3c")))  # Set background color        
        self.tree_widget.addTopLevelItem(item)



    def enable_candidates_page(self):
        """Enable the Candidates Management page after successful login."""
        self.tree_widget.topLevelItem(1).setDisabled(False)  # Enable "Candidates Page" item
        self.stacked_widget.setCurrentIndex(1)  # Automatically switch to Candidates Management page
        self.tree_widget.topLevelItem(0).setDisabled(True)

    def handle_logout(self):
        """Handle logout logic."""
        self.tree_widget.topLevelItem(1).setDisabled(True)  # Disable "Candidates Page"
        self.stacked_widget.setCurrentIndex(0)  # Switch to login page
        QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")
        self.tree_widget.topLevelItem(0).setDisabled(False)

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
