# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
#     QLineEdit, QSpinBox, QComboBox, QPushButton, QTableWidget,
#     QTableWidgetItem, QMessageBox
# )
# from sqlmodel import Session, select
# from sqlalchemy.orm import joinedload
# from sqlalchemy.orm import sessionmaker
# from models import Candidate, Certificate, Qualification, Skill, engine

# # Create database session
# SessionLocal = sessionmaker(bind=engine)


# class CandidateManager(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Candidate Manager")
#         self.setGeometry(200, 200, 800, 600)

#         # Main container
#         self.container = QWidget()
#         self.layout = QVBoxLayout()

#         # Add Candidate Section
#         self.add_candidate_section()

#         # Search Section
#         self.search_section()

#         # Set up the main widget and layout
#         self.container.setLayout(self.layout)
#         self.setCentralWidget(self.container)

#         # Load dropdown options
#         self.load_dropdowns()

#         # Load all candidates initially
#         self.load_all_candidates()

#     def add_candidate_section(self):
#         form_layout = QFormLayout()

#         # Candidate Details
#         self.name_input = QLineEdit()
#         self.email_input = QLineEdit()
#         self.experience_input = QSpinBox()
#         self.experience_input.setRange(0, 50)

#         # Manual entry fields for certificates, qualifications, and skills
#         self.certificate_input = QLineEdit()
#         self.qualification_input = QLineEdit()
#         self.skill_input = QLineEdit()

#         form_layout.addRow("Name:", self.name_input)
#         form_layout.addRow("Email:", self.email_input)
#         form_layout.addRow("Experience Years:", self.experience_input)
#         form_layout.addRow("Certificates (comma-separated):", self.certificate_input)
#         form_layout.addRow("Qualifications (comma-separated):", self.qualification_input)
#         form_layout.addRow("Skills (comma-separated):", self.skill_input)

#         # Add button
#         add_button = QPushButton("Add Candidate")
#         add_button.clicked.connect(self.add_candidate)
#         form_layout.addWidget(add_button)

#         self.layout.addLayout(form_layout)

#     def search_section(self):
#         search_layout = QFormLayout()

#         self.search_experience_input = QSpinBox()
#         self.search_experience_input.setRange(0, 50)
#         self.search_certificates_dropdown = QComboBox()
#         self.search_qualifications_dropdown = QComboBox()
#         self.search_skills_dropdown = QComboBox()

#         # Load dropdown options
#         self.load_dropdowns(search=True)

#         search_layout.addRow("Experience Years:", self.search_experience_input)
#         search_layout.addRow("Certificates:", self.search_certificates_dropdown)
#         search_layout.addRow("Qualifications:", self.search_qualifications_dropdown)
#         search_layout.addRow("Skills:", self.search_skills_dropdown)

#         # Search button
#         search_button = QPushButton("Search Candidates")
#         search_button.clicked.connect(self.search_candidates)
#         search_layout.addWidget(search_button)

#         # Results table
#         self.results_table = QTableWidget(0, 6)  # 6 columns
#         self.results_table.setHorizontalHeaderLabels([
#             "Name", "Email", "Experience Years", "Certificates", "Qualifications", "Skills"
#         ])

#         self.layout.addLayout(search_layout)
#         self.layout.addWidget(self.results_table)

#     def load_dropdowns(self, search=False):
#         with Session(engine) as session:
#             certificates = session.query(Certificate).all()
#             qualifications = session.query(Qualification).all()
#             skills = session.query(Skill).all()

#         if search:
#             dropdowns = {
#                 "certificates": self.search_certificates_dropdown,
#                 "qualifications": self.search_qualifications_dropdown,
#                 "skills": self.search_skills_dropdown,
#             }
#         else:
#             return  # Only load for search dropdowns

#         for category, dropdown in dropdowns.items():
#             dropdown.clear()
#             dropdown.addItem("None")
#             items = {
#                 "certificates": certificates,
#                 "qualifications": qualifications,
#                 "skills": skills,
#             }.get(category, [])
#             for item in items:
#                 dropdown.addItem(item.name)


#     def load_all_candidates(self):
#         with Session(engine) as session:
#             # Eagerly load certificates, qualifications, and skills using joinedload
#             candidates = session.query(Candidate).options(
#                 joinedload(Candidate.certificates),
#                 joinedload(Candidate.extra_qualifications),
#                 joinedload(Candidate.skills)
#             ).all()

#         self.results_table.setRowCount(len(candidates))
#         for row, candidate in enumerate(candidates):
#             self.results_table.setItem(row, 0, QTableWidgetItem(candidate.name))
#             self.results_table.setItem(row, 1, QTableWidgetItem(candidate.email))
#             self.results_table.setItem(row, 2, QTableWidgetItem(str(candidate.experience_years)))
#             # Combine names of certificates, qualifications, and skills into comma-separated strings
#             certificates = ", ".join([cert.name for cert in candidate.certificates])
#             qualifications = ", ".join([qual.name for qual in candidate.extra_qualifications])
#             skills = ", ".join([skill.name for skill in candidate.skills])

#             self.results_table.setItem(row, 3, QTableWidgetItem(certificates))
#             self.results_table.setItem(row, 4, QTableWidgetItem(qualifications))
#             self.results_table.setItem(row, 5, QTableWidgetItem(skills))


#     def add_candidate(self):
#         name = self.name_input.text()
#         email = self.email_input.text()
#         experience = self.experience_input.value()
#         certificates = [x.strip() for x in self.certificate_input.text().split(",") if x.strip()]
#         qualifications = [x.strip() for x in self.qualification_input.text().split(",") if x.strip()]
#         skills = [x.strip() for x in self.skill_input.text().split(",") if x.strip()]

#         if not name:
#             QMessageBox.warning(self, "Error", "Name cannot be empty!")
#             return

#         with Session(engine) as session:
#             candidate = Candidate(name=name, email=email, experience_years=experience)

#             for cert_name in certificates:
#                 certificate = session.query(Certificate).filter(Certificate.name == cert_name).first()
#                 if not certificate:
#                     certificate = Certificate(name=cert_name)
#                     session.add(certificate)
#                 candidate.certificates.append(certificate)

#             for qual_name in qualifications:
#                 qualification = session.query(Qualification).filter(Qualification.name == qual_name).first()
#                 if not qualification:
#                     qualification = Qualification(name=qual_name)
#                     session.add(qualification)
#                 candidate.extra_qualifications.append(qualification)

#             for skill_name in skills:
#                 skill = session.query(Skill).filter(Skill.name == skill_name).first()
#                 if not skill:
#                     skill = Skill(name=skill_name)
#                     session.add(skill)
#                 candidate.skills.append(skill)

#             session.add(candidate)
#             session.commit()
#             QMessageBox.information(self, "Success", "Candidate added successfully!")
#             self.name_input.clear()
#             self.email_input.clear()
#             self.experience_input.setValue(0)
#             self.certificate_input.clear()
#             self.qualification_input.clear()
#             self.skill_input.clear()

#         # Reload all candidates after adding a new one
#         self.load_all_candidates()

#     def search_candidates(self):
#         experience = self.search_experience_input.value()
#         certificate_name = self.search_certificates_dropdown.currentText()
#         qualification_name = self.search_qualifications_dropdown.currentText()
#         skill_name = self.search_skills_dropdown.currentText()

#         query = session.query(Candidate).filter(Candidate.experience_years >= experience)

#         with Session(engine) as session:
#             # Eagerly load related data for the search
#             query = query.options(
#                 joinedload(Candidate.certificates),
#                 joinedload(Candidate.extra_qualifications),
#                 joinedload(Candidate.skills)
#             )

#             if certificate_name != "None":
#                 query = query.filter(Candidate.certificates.any(Certificate.name == certificate_name))
#             if qualification_name != "None":
#                 query = query.filter(Candidate.extra_qualifications.any(Qualification.name == qualification_name))
#             if skill_name != "None":
#                 query = query.filter(Candidate.skills.any(Skill.name == skill_name))

#             results = query.all()

#         self.results_table.setRowCount(len(results))
#         for row, candidate in enumerate(results):
#             self.results_table.setItem(row, 0, QTableWidgetItem(candidate.name))
#             self.results_table.setItem(row, 1, QTableWidgetItem(candidate.email))
#             self.results_table.setItem(row, 2, QTableWidgetItem(str(candidate.experience_years)))
#             # Combine names of certificates, qualifications, and skills into comma-separated strings
#             certificates = ", ".join([cert.name for cert in candidate.certificates])
#             qualifications = ", ".join([qual.name for qual in candidate.extra_qualifications])
#             skills = ", ".join([skill.name for skill in candidate.skills])

#             self.results_table.setItem(row, 3, QTableWidgetItem(certificates))
#             self.results_table.setItem(row, 4, QTableWidgetItem(qualifications))
#             self.results_table.setItem(row, 5, QTableWidgetItem(skills))

# # Run the Application
# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)
#     window = CandidateManager()
#     window.show()
#     sys.exit(app.exec_())
