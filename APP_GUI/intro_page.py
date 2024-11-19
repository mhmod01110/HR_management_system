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
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt

class CreateCandidateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Candidate")

        # Layout for the form
        layout = QVBoxLayout()

        # Form layout for candidate data input
        form_layout = QFormLayout()

        # Input fields
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_num_input = QLineEdit()
        self.experience_years_input = QSpinBox()
        self.experience_years_input.setMinimum(0)
        self.experience_years_input.setMaximum(50)

        # List fields for certificates, qualifications, and skills
        self.certificates_input = QLineEdit()
        self.qualifications_input = QLineEdit()
        self.skills_input = QLineEdit()

        # Instructions for list fields
        list_instructions = QLabel("Enter items separated by commas (e.g., 'Cert1, Cert2').")

        # Add input fields to the form
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_num_input)
        form_layout.addRow("Experience Years:", self.experience_years_input)
        form_layout.addRow("Certificates:", self.certificates_input)
        form_layout.addRow("Qualifications:", self.qualifications_input)
        form_layout.addRow("Skills:", self.skills_input)

        # Buttons for submitting or canceling
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Add widgets to the dialog layout
        layout.addWidget(list_instructions)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_candidate_data(self):
        """Return the candidate data entered in the dialog."""
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone_num': self.phone_num_input.text(),
            'experience_years': self.experience_years_input.value(),
            'certificates': [item.strip() for item in self.certificates_input.text().split(",") if item.strip()],
            'qualifications': [item.strip() for item in self.qualifications_input.text().split(",") if item.strip()],
            'skills': [item.strip() for item in self.skills_input.text().split(",") if item.strip()],
        }


class UpdateCandidateDialog(CreateCandidateDialog):
    def __init__(self, candidate_data):
        super().__init__()
        self.setWindowTitle("Update Candidate")

        # Pre-fill the fields with existing candidate data
        self.name_input.setText(candidate_data.get("name", ""))
        self.email_input.setText(candidate_data.get("email", ""))
        self.phone_num_input.setText(candidate_data.get("phone_num", ""))
        self.experience_years_input.setValue(candidate_data.get("experience_years", 0))
        self.certificates_input.setText(", ".join(candidate_data.get("certificates", [])))
        self.qualifications_input.setText(", ".join(candidate_data.get("qualifications", [])))
        self.skills_input.setText(", ".join(candidate_data.get("skills", [])))


class CandidatesManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(self.create_layout())

    def create_layout(self):
        """Set up the layout for the candidates page."""
        layout = QVBoxLayout()

        # Title Label
        label = QLabel("Candidates Management")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: black;")
        layout.addWidget(label)

        # Table to show candidates
        self.candidate_table = QTableWidget()
        self.candidate_table.setColumnCount(6)
        self.candidate_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Email", "Phone Number", "Experience Years", "Certificates"]
        )
        self.populate_candidate_table()
        layout.addWidget(self.candidate_table)

        # Buttons for CRUD operations
        self.create_candidate_button = QPushButton("Create Candidate")
        self.update_candidate_button = QPushButton("Update Candidate")
        self.delete_candidate_button = QPushButton("Delete Candidate")

        self.create_candidate_button.clicked.connect(self.show_create_candidate_dialog)
        self.update_candidate_button.clicked.connect(self.update_candidate)
        self.delete_candidate_button.clicked.connect(self.delete_candidate)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_candidate_button)
        button_layout.addWidget(self.update_candidate_button)
        button_layout.addWidget(self.delete_candidate_button)
        layout.addLayout(button_layout)

        return layout

    def populate_candidate_table(self):
        """Populate the candidates table with data from the database."""
        candidates = get_all_candidates_interface()
        self.candidate_table.setRowCount(len(candidates))
        for row, candidate in enumerate(candidates):
            self.candidate_table.setItem(row, 0, QTableWidgetItem(str(candidate.id)))
            self.candidate_table.setItem(row, 1, QTableWidgetItem(candidate.name))
            self.candidate_table.setItem(row, 2, QTableWidgetItem(candidate.email or "N/A"))
            self.candidate_table.setItem(row, 3, QTableWidgetItem(candidate.phone_num or "N/A"))
            self.candidate_table.setItem(row, 4, QTableWidgetItem(str(candidate.experience_years)))
            certificates = ", ".join([cert.name for cert in candidate.certificates])
            self.candidate_table.setItem(row, 5, QTableWidgetItem(certificates or "N/A"))

    def show_create_candidate_dialog(self):
        """Show the Create Candidate dialog."""
        dialog = CreateCandidateDialog()
        if dialog.exec() == QDialog.Accepted:
            candidate_data = dialog.get_candidate_data()
            create_candidate_interface(**candidate_data)
            self.populate_candidate_table()

    def update_candidate(self):
        """Update a selected candidate."""
        selected_row = self.candidate_table.currentRow()
        if selected_row >= 0:
            candidate_id = int(self.candidate_table.item(selected_row, 0).text())
            candidate_data = get_candidate_by_id_interface(candidate_id)
            dialog = UpdateCandidateDialog(candidate_data)
            if dialog.exec() == QDialog.Accepted:
                updated_data = dialog.get_candidate_data()
                update_candidate_interface(candidate_id, **updated_data)
                self.populate_candidate_table()

    def delete_candidate(self):
        """Delete a selected candidate."""
        selected_row = self.candidate_table.currentRow()
        if selected_row >= 0:
            candidate_id = int(self.candidate_table.item(selected_row, 0).text())
            delete_candidate_interface(candidate_id)
            self.populate_candidate_table()
