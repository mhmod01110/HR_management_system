import sys
import os

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from users_orders_manager
from candidates_data_handler.interface import *
from sqlalchemy import or_, and_

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QPushButton, QFormLayout, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDialogButtonBox, QSpinBox, QMessageBox, QFileDialog
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
        
class EditCandidateDialog(QDialog):
    def __init__(self, candidate_data):
        super().__init__()
        self.setWindowTitle("Edit Candidate")

        # Layout for the form
        layout = QVBoxLayout()

        # Form layout for candidate data input
        form_layout = QFormLayout()

        # Create input fields with existing candidate data
        self.name_input = QLineEdit(candidate_data.name if hasattr(candidate_data, 'name') else "")
        self.email_input = QLineEdit(candidate_data.email if hasattr(candidate_data, 'email') else "")
        self.phone_num_input = QLineEdit(candidate_data.phone_num if hasattr(candidate_data, 'phone_num') else "")
        
        self.experience_years_input = QSpinBox()
        self.experience_years_input.setMinimum(0)
        self.experience_years_input.setMaximum(50)
        self.experience_years_input.setValue(candidate_data.experience_years if hasattr(candidate_data, 'experience_years') else 0)
        
        # Convert Certificate, Qualification, and Skill objects to string (extract 'name')
        certificates = getattr(candidate_data, 'certificates', [])
        self.certificates_input = QLineEdit(", ".join(cert.name for cert in certificates))  # Use cert.name for string representation
        
        qualifications = getattr(candidate_data, 'extra_qualifications', [])
        self.qualifications_input = QLineEdit(", ".join(q.name for q in qualifications))  # Use q.name for string representation
        
        skills = getattr(candidate_data, 'skills', [])
        self.skills_input = QLineEdit(", ".join(s.name for s in skills))  # Use s.name for string representation

        # Add the input fields to the form layout
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

        # Add form layout and buttons to the dialog layout
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_candidate_data(self):
        """Return the updated candidate data."""
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone_num': self.phone_num_input.text(),
            'experience_years': self.experience_years_input.value(),
            'certificates': self.certificates_input.text().split(", "),
            'qualifications': self.qualifications_input.text().split(", "),
            'skills': self.skills_input.text().split(", ")
        }


class CandidateSearchDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Search Candidates")
        self.session = session  # SQLAlchemy session passed to interact with the database

        # Layout for the form
        layout = QVBoxLayout()

        # Form layout for search input fields
        form_layout = QFormLayout()

        # Name field for searching
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)

        # Email field for searching
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)

        # Skills field - Multi-selection combobox (OR condition)
        self.skills_input = QComboBox()
        self.skills_input.setEditable(True)  # Set editable for custom input
        self.skills_input.addItems(self.get_skills_from_db())
        form_layout.addRow("Skills:", self.skills_input)

        # Qualifications field - Multi-selection combobox (OR condition)
        self.qualifications_input = QComboBox()
        self.qualifications_input.setEditable(True)
        self.qualifications_input.addItems(self.get_qualifications_from_db())
        form_layout.addRow("Qualifications:", self.qualifications_input)

        # Experience Years (you can add more search criteria like this)
        self.experience_years_input = QSpinBox()
        self.experience_years_input.setMinimum(0)
        form_layout.addRow("Experience Years:", self.experience_years_input)

        # Buttons for submitting or canceling the search
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.search_candidates)
        button_box.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_skills_from_db(self):
        """Fetch skills from the database to populate the skills combo box."""
        skills = self.session.query(Skill).all()
        return [skill.name for skill in skills]

    def get_qualifications_from_db(self):
        """Fetch qualifications from the database to populate the qualifications combo box."""
        qualifications = self.session.query(Qualification).all()
        return [qualification.name for qualification in qualifications]

    def search_candidates(self):
        """Search candidates based on the entered criteria."""
        # Build the base query
        query = self.session.query(Candidate)

        # Apply name filter (AND condition)
        name = self.name_input.text()
        if name:
            query = query.filter(Candidate.name.ilike(f"%{name}%"))

        # Apply email filter (AND condition)
        email = self.email_input.text()
        if email:
            query = query.filter(Candidate.email.ilike(f"%{email}%"))

        # Apply skills filter (OR condition for multiple selected skills)
        skills_selected = self.skills_input.currentText().split(", ")
        if skills_selected:
            skill_filters = [Candidate.skills.any(Skill.name.ilike(f"%{skill}%")) for skill in skills_selected]
            query = query.filter(or_(*skill_filters))

        # Apply qualifications filter (OR condition for multiple selected qualifications)
        qualifications_selected = self.qualifications_input.currentText().split(", ")
        if qualifications_selected:
            qualification_filters = [Candidate.extra_qualifications.any(Qualification.name.ilike(f"%{qualification}%")) for qualification in qualifications_selected]
            query = query.filter(or_(*qualification_filters))

        # Apply experience years filter (AND condition)
        experience_years = self.experience_years_input.value()
        if experience_years:
            query = query.filter(Candidate.experience_years >= experience_years)

        # Execute the query and get the results
        self.candidates = query.all()  # Store the results in self.candidates

        # Print results for now (you can display them in a table or a list view)
        for candidate in self.candidates:
            print(candidate.name, candidate.email, candidate.experience_years)

        # Close the dialog after search
        self.accept()

    def get_search_results(self):
        """Return the filtered search results."""
        return self.candidates  # Return the stored candidates list

class CandidatesManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(self.create_layout())
        self.session = session

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
        self.candidate_table.setColumnCount(8)
        self.candidate_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Email", "Phone Number", "Experience Years", "Certificates", "Qualifications", "Skills"]
        )
        self.candidate_table.setStyleSheet("background-color: white;")
        self.populate_candidate_table()
        layout.addWidget(self.candidate_table)

        # Buttons for CRUD operations
        self.create_candidate_button = QPushButton("Create Candidate")
        self.edit_candidate_button = QPushButton("Edit Candidate")
        self.delete_candidate_button = QPushButton("Delete Candidate")
        self.export_csv_button = QPushButton("Export to CSV")
        self.search_candidate_button = QPushButton("Search Candidate")

        self.create_candidate_button.clicked.connect(self.show_create_candidate_dialog)
        self.edit_candidate_button.clicked.connect(self.edit_candidate)
        self.delete_candidate_button.clicked.connect(self.delete_candidate)
        self.export_csv_button.clicked.connect(self.export_csv)
        self.search_candidate_button.clicked.connect(self.search_candidate)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_candidate_button)
        button_layout.addWidget(self.edit_candidate_button)
        button_layout.addWidget(self.delete_candidate_button)
        button_layout.addWidget(self.export_csv_button)
        button_layout.addWidget(self.search_candidate_button)
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
            qualifications = ", ".join([qual.name for qual in candidate.extra_qualifications])
            self.candidate_table.setItem(row, 6, QTableWidgetItem(qualifications or "N/A"))
            skills = ", ".join([skill.name for skill in candidate.skills])
            self.candidate_table.setItem(row, 7, QTableWidgetItem(skills or "N/A"))
            
    def show_create_candidate_dialog(self):
        """Show the Create Candidate dialog."""
        dialog = CreateCandidateDialog()
        if dialog.exec() == QDialog.Accepted:
            candidate_data = dialog.get_candidate_data()
            create_candidate_interface(**candidate_data)
            self.populate_candidate_table()

    def edit_candidate(self):
        """edit a selected candidate."""
        selected_row = self.candidate_table.currentRow()
        if selected_row >= 0:
            candidate_id = int(self.candidate_table.item(selected_row, 0).text())
            candidate_data = get_candidate_by_id_interface(candidate_id)
            dialog = EditCandidateDialog(candidate_data)
            if dialog.exec() == QDialog.Accepted:
                editd_data = dialog.get_candidate_data()
                edit_candidate_interface(candidate_id, **editd_data)
                self.populate_candidate_table()

    def delete_candidate(self):
        """Delete a selected candidate."""
        selected_row = self.candidate_table.currentRow()
        if selected_row >= 0:
            candidate_id = int(self.candidate_table.item(selected_row, 0).text())
            delete_candidate_interface(candidate_id)
            self.populate_candidate_table()


    def export_csv(self):
        """Export candidate data to a CSV file with a selected file path."""
        # Open file dialog to get the file path
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        
        if file_path:
            # Proceed with exporting to the selected file path
            export_candidates_to_csv_interface(file_path=file_path)
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")


    def search_candidate(self):
        """Open the Search Candidate dialog and perform the search operation."""
        dialog = CandidateSearchDialog(self.session)
        if dialog.exec() == QDialog.Accepted:
            # If search criteria are entered, update the table with search results
            search_results = dialog.get_search_results()  # Assuming you will add a method to return results
            self.update_candidate_table(search_results)

    def update_candidate_table(self, candidates):
        """Update the table with search results."""
        self.candidate_table.setRowCount(len(candidates))
        for row, candidate in enumerate(candidates):
            self.candidate_table.setItem(row, 0, QTableWidgetItem(str(candidate.id)))
            self.candidate_table.setItem(row, 1, QTableWidgetItem(candidate.name))
            self.candidate_table.setItem(row, 2, QTableWidgetItem(candidate.email or "N/A"))
            self.candidate_table.setItem(row, 3, QTableWidgetItem(candidate.phone_num or "N/A"))
            self.candidate_table.setItem(row, 4, QTableWidgetItem(str(candidate.experience_years)))
            certificates = ", ".join([cert.name for cert in candidate.certificates])
            self.candidate_table.setItem(row, 5, QTableWidgetItem(certificates or "N/A"))
            qualifications = ", ".join([qual.name for qual in candidate.extra_qualifications])
            self.candidate_table.setItem(row, 6, QTableWidgetItem(qualifications or "N/A"))
            skills = ", ".join([skill.name for skill in candidate.skills])
            self.candidate_table.setItem(row, 7, QTableWidgetItem(skills or "N/A"))

