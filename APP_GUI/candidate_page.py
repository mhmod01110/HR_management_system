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
    QDialog, QLineEdit, QComboBox, QDialogButtonBox, QSpinBox, QMessageBox, QFileDialog,
    QListWidget, QAbstractItemView, QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt

class CreateCandidateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ادخل مرشح جديد للنظام")

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
        list_instructions = QLabel("ادخل العناصر (الشهادات - المؤهلات - المهارات) مفصول بينهم بفاصل , : مثال (عنصر1 , عنصر2 , ..)")

        # Add the input fields to the form layout
        form_layout.addRow(QLabel(": الاسم"), self.name_input)
        form_layout.addRow(QLabel(": البريد الالكتروني"), self.email_input)
        form_layout.addRow(QLabel(": رقم الهاتف"), self.phone_num_input)
        form_layout.addRow(QLabel(": سنوات الخبرة"), self.experience_years_input)
        form_layout.addRow(QLabel(": الشهادات"), self.certificates_input)
        form_layout.addRow(QLabel(": المؤهلات الاضافية"), self.qualifications_input)
        form_layout.addRow(QLabel(": المهارات"), self.skills_input)


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
        self.setWindowTitle("تعديل المرشح")

        # Layout for the form
        layout = QVBoxLayout()

        # Form layout for candidate data input
        form_layout = QFormLayout()

        # Helper function to dynamically adjust field size
        def adjust_field_size(field):
            field.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            field.textChanged.connect(lambda: field.setFixedWidth(field.fontMetrics().boundingRect(field.text()).width() + 20))

        # Create input fields with existing candidate data
        self.name_input = QLineEdit(candidate_data.name if hasattr(candidate_data, 'name') else "")
        adjust_field_size(self.name_input)

        self.email_input = QLineEdit(candidate_data.email if hasattr(candidate_data, 'email') else "")
        adjust_field_size(self.email_input)

        self.phone_num_input = QLineEdit(candidate_data.phone_num if hasattr(candidate_data, 'phone_num') else "")
        adjust_field_size(self.phone_num_input)

        self.experience_years_input = QSpinBox()
        self.experience_years_input.setMinimum(0)
        self.experience_years_input.setMaximum(50)
        self.experience_years_input.setValue(candidate_data.experience_years if hasattr(candidate_data, 'experience_years') else 0)

        # Convert Certificate, Qualification, and Skill objects to string (extract 'name')
        certificates = getattr(candidate_data, 'certificates', [])
        self.certificates_input = QLineEdit(", ".join(cert.name for cert in certificates))
        adjust_field_size(self.certificates_input)

        qualifications = getattr(candidate_data, 'extra_qualifications', [])
        self.qualifications_input = QLineEdit(", ".join(q.name for q in qualifications))
        adjust_field_size(self.qualifications_input)

        skills = getattr(candidate_data, 'skills', [])
        self.skills_input = QLineEdit(", ".join(s.name for s in skills))
        adjust_field_size(self.skills_input)

        # Add the input fields to the form layout
        form_layout.addRow(QLabel(": الاسم"), self.name_input)
        form_layout.addRow(QLabel(": البريد الالكتروني"), self.email_input)
        form_layout.addRow(QLabel(": رقم الهاتف"), self.phone_num_input)
        form_layout.addRow(QLabel(": سنوات الخبرة"), self.experience_years_input)
        form_layout.addRow(QLabel(": الشهادات"), self.certificates_input)
        form_layout.addRow(QLabel(": المؤهلات الاضافية"), self.qualifications_input)
        form_layout.addRow(QLabel(": المهارات"), self.skills_input)

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
        self.setWindowTitle("البحث عن مرشح")
        self.session = session  # SQLAlchemy session passed to interact with the database

        # Layout for the form
        layout = QVBoxLayout()

        # Form layout for search input fields
        form_layout = QFormLayout()

        # Name field for searching
        self.name_input = QLineEdit()
        form_layout.addRow(self.name_input, QLabel("الاسم:"))

        # Email field for searching
        self.email_input = QLineEdit()
        form_layout.addRow(self.email_input, QLabel("البريد الالكتروني:"))

        # Skills field - Multi-selection list widget
        self.skills_input = QListWidget()
        self.skills_input.setSelectionMode(QAbstractItemView.MultiSelection)
        self.populate_list_widget(self.skills_input, self.get_skills_from_db())
        form_layout.addRow(self.skills_input, QLabel("المهارات:"))

        # Qualifications field - Multi-selection list widget
        self.qualifications_input = QListWidget()
        self.qualifications_input.setSelectionMode(QAbstractItemView.MultiSelection)
        self.populate_list_widget(self.qualifications_input, self.get_qualifications_from_db())
        form_layout.addRow(self.qualifications_input, QLabel("المؤهلات الاضافية:"))

        # Certificates field - Multi-selection list widget
        self.certificates_input = QListWidget()
        self.certificates_input.setSelectionMode(QAbstractItemView.MultiSelection)
        self.populate_list_widget(self.certificates_input, self.get_certificates_from_db())
        form_layout.addRow(self.certificates_input, QLabel("الشهادات:"))

        # Experience Years
        self.experience_years_input = QSpinBox()
        self.experience_years_input.setMinimum(0)
        form_layout.addRow(self.experience_years_input, QLabel("سنوات الخبرة:"))
        # Buttons for submitting or canceling the search
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.search_candidates)
        button_box.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def populate_list_widget(self, widget, items):
        """Populate a QListWidget with items."""
        for item in items:
            widget.addItem(item)

    def get_skills_from_db(self):
        skills = self.session.query(Skill).all()
        return [skill.name for skill in skills]

    def get_qualifications_from_db(self):
        qualifications = self.session.query(Qualification).all()
        return [qualification.name for qualification in qualifications]

    def get_certificates_from_db(self):
        certificates = self.session.query(Certificate).all()
        return [certificate.name for certificate in certificates]
    
    def search_candidates(self):
        """Search candidates based on the entered criteria."""
        # Start with the base query
        query = self.session.query(Candidate)

        # Apply name filter
        name = self.name_input.text()
        if name:
            query = query.filter(Candidate.name.ilike(f"%{name}%"))

        # Apply email filter
        email = self.email_input.text()
        if email:
            query = query.filter(Candidate.email.ilike(f"%{email}%"))

        # Apply skills filter (AND condition for all selected skills)
        selected_skills = [item.text() for item in self.skills_input.selectedItems()]
        if selected_skills:
            for skill in selected_skills:
                query = query.filter(Candidate.skills.any(Skill.name.ilike(f"%{skill}%")))

        # Apply qualifications filter (AND condition for all selected qualifications)
        selected_qualifications = [item.text() for item in self.qualifications_input.selectedItems()]
        if selected_qualifications:
            for qualification in selected_qualifications:
                query = query.filter(Candidate.extra_qualifications.any(Qualification.name.ilike(f"%{qualification}%")))

        # Apply certificates filter (AND condition for all selected certificates)
        selected_certificates = [item.text() for item in self.certificates_input.selectedItems()]
        if selected_certificates:
            for certificate in selected_certificates:
                query = query.filter(Candidate.certificates.any(Certificate.name.ilike(f"%{certificate}%")))

        # Apply experience years filter
        experience_years = self.experience_years_input.value()
        if experience_years > 0:
            query = query.filter(Candidate.experience_years >= experience_years)

        # Execute the query and get the results
        self.candidates = query.all()

        # Print results for testing (you can update this to display in the GUI)
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
        label = QLabel("إدارة المرشحين")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: black;")
        layout.addWidget(label)

        # Table to show candidates
        self.candidate_table = QTableWidget()
        self.candidate_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.candidate_table.setColumnCount(8)
        self.candidate_table.setHorizontalHeaderLabels(
            ["الرقم التعريفي", "الاسم", "البريد الالكتروني", "رقم الهاتف", "سنوات الخبرة", "الشهادات", "المؤهلات الاضافية", "المهارات"]
        )
        self.candidate_table.setStyleSheet("background-color: white;")
        self.candidate_table.horizontalHeader().setStyleSheet("background-color: lightgray; font-size: 16;")
        self.candidate_table.verticalHeader().setStyleSheet("background-color: lightgray; font-size: 16;")
        # Enable auto-resize for columns and rows
        self.candidate_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.candidate_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.candidate_table.resizeColumnsToContents()
        self.candidate_table.resizeRowsToContents()
        # Enable word wrapping
        self.candidate_table.setWordWrap(True)
        self.candidate_table.setFont(QFont("Arial", 12))
        self.populate_candidate_table()
        layout.addWidget(self.candidate_table)

        # Buttons for CRUD operations
        button_style = """
            QPushButton {
                background-color: orange;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #d17817; /* Slightly darker orange on hover */
            }
            QPushButton:pressed {
                background-color: #e68a00; /* Even darker orange when pressed */
            }
        """
        
        self.create_candidate_button = QPushButton("ادخل مرشح جديد")
        self.create_candidate_button.setStyleSheet(button_style)
        self.create_candidate_button.setMinimumHeight(50)  # Make buttons larger

        self.edit_candidate_button = QPushButton("تعديل مرشح")
        self.edit_candidate_button.setStyleSheet(button_style)
        self.edit_candidate_button.setMinimumHeight(50)

        self.delete_candidate_button = QPushButton("حذف المرشح")
        self.delete_candidate_button.setStyleSheet(button_style)
        self.delete_candidate_button.setMinimumHeight(50)

        self.export_csv_button = QPushButton("تصدير البيانات CSV")
        self.export_csv_button.setStyleSheet(button_style)
        self.export_csv_button.setMinimumHeight(50)

        self.search_candidate_button = QPushButton("البحث عن مرشح")
        self.search_candidate_button.setStyleSheet(button_style)
        self.search_candidate_button.setMinimumHeight(50)

        self.clear_filters_button = QPushButton("عرض جميع المرشحين")
        self.clear_filters_button.setStyleSheet(button_style)
        self.clear_filters_button.setMinimumHeight(50)


        self.create_candidate_button.clicked.connect(self.show_create_candidate_dialog)
        self.edit_candidate_button.clicked.connect(self.edit_candidate)
        self.delete_candidate_button.clicked.connect(self.delete_candidate)
        self.export_csv_button.clicked.connect(self.export_csv)
        self.search_candidate_button.clicked.connect(self.search_candidate)
        self.clear_filters_button.clicked.connect(self.clear_filters)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_candidate_button)
        button_layout.addWidget(self.edit_candidate_button)
        button_layout.addWidget(self.delete_candidate_button)
        button_layout.addWidget(self.export_csv_button)
        button_layout.addWidget(self.search_candidate_button)
        button_layout.addWidget(self.clear_filters_button)
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
        """Delete selected candidates."""
        # Get selected rows
        selected_items = self.candidate_table.selectedItems()
        if selected_items:
            # Extract unique row indices from the selected items
            selected_rows = list(set(item.row() for item in selected_items))
            selected_rows.sort(reverse=True)  # Sort in reverse to avoid shifting indices during deletion

            # Gather candidate details for confirmation
            candidates_to_delete = []
            for row in selected_rows:
                candidate_id = int(self.candidate_table.item(row, 0).text())
                candidate_name = self.candidate_table.item(row, 1).text()
                candidates_to_delete.append((candidate_id, candidate_name))

            # Create a confirmation dialog
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Warning)
            confirmation.setWindowTitle("تأكيد الحذف")
            candidate_names = ", ".join([f"'{name}'" for _, name in candidates_to_delete])
            confirmation.setText(f"هل أنت متأكد من حذف المرشحين التاليين: {candidate_names}?")
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation.setDefaultButton(QMessageBox.No)

            if confirmation.exec() == QMessageBox.Yes:
                # Delete candidates
                for candidate_id, _ in candidates_to_delete:
                    delete_candidate_interface(candidate_id)
                self.populate_candidate_table()



    def export_csv(self):
        """Export visible candidate data from the table to a CSV file."""
        # Open file dialog to get the file path
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options
        )

        if file_path:
            # Open the file for writing
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write the header row
                headers = [self.candidate_table.horizontalHeaderItem(col).text()
                        for col in range(self.candidate_table.columnCount())]
                writer.writerow(headers)

                # Write the data rows for visible candidates
                for row in range(self.candidate_table.rowCount()):
                    row_data = [
                        self.candidate_table.item(row, col).text()
                        if self.candidate_table.item(row, col) else ""
                        for col in range(self.candidate_table.columnCount())
                    ]
                    writer.writerow(row_data)

            QMessageBox.information(self, "تم التصدير بنجاح", f"تم تصدير البيانات إلى : {file_path}")


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

    def clear_filters(self):
        """Clear the search filters and reset the table."""
        self.populate_candidate_table()  # Repopulate the table with all candidates
        # QMessageBox.information(self, "Filters Cleared", "Search filters have been cleared.")
