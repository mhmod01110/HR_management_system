import os
import sys
# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from candidates_data_handler.models import *
from candidates_data_handler.candidate_manager import *


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

candidate_manager = CandidateManager(session)

# Use Case 1: Create a Candidate
def create_candidate_interface(
    name: str, 
    email: Optional[str], 
    phone_num: Optional[str], 
    experience_years: int,
    certificates: Optional[List[str]] = None,
    qualifications: Optional[List[str]] = None,
    skills: Optional[List[str]] = None,
):
    try:
        candidate = candidate_manager.create_candidate(
            name=name,
            email=email,
            phone_num=phone_num,
            experience_years=experience_years,
            certificates=certificates,
            qualifications=qualifications,
            skills=skills,
        )
        return candidate
    except ValueError as e:
        print(f"Error: {e}")
        return None


# Use Case 2: Get Candidate by ID
def get_candidate_by_id_interface(candidate_id: int):
    candidate = candidate_manager.get_by_id(candidate_id)
    if candidate:
        return candidate
    else:
        print(f"No candidate found with ID {candidate_id}")
        return None


# Use Case 3: Get All Candidates
def get_all_candidates_interface():
    candidates = candidate_manager.get_all()
    return candidates


# Use Case 4: edit Candidate by ID
def edit_candidate_interface(
    candidate_id: int, 
    name: Optional[str] = None, 
    email: Optional[str] = None, 
    phone_num: Optional[str] = None, 
    experience_years: Optional[int] = None,
    certificates: Optional[List[str]] = None,
    qualifications: Optional[List[str]] = None,
    skills: Optional[List[str]] = None,
):
    try:
        candidate = candidate_manager.edit_by_id(
            candidate_id,
            name=name,
            email=email,
            phone_num=phone_num,
            experience_years=experience_years,
            certificates=certificates,
            qualifications=qualifications,
            skills=skills,
        )
        if candidate:
            return candidate
        else:
            print(f"No candidate found with ID {candidate_id}")
            return None
    except ValueError as e:
        print(f"Error: {e}")
        return None


# Use Case 5: Delete Candidate
def delete_candidate_interface(candidate_id: int):
    success = candidate_manager.delete(candidate_id)
    if success:
        print(f"Candidate with ID {candidate_id} deleted successfully.")
        return True
    else:
        print(f"No candidate found with ID {candidate_id}")
        return False


# Use Case 6: Export Candidates to CSV
def export_candidates_to_csv_interface(file_path: str):
    try:
        candidate_manager.export_to_csv(file_path)
        print(f"Candidates exported to {file_path} successfully.")
    except Exception as e:
        print(f"Error exporting candidates: {e}")


# Use Case: Print All Candidates
def print_all_candidates_interface():
    candidates = candidate_manager.get_all()

    if not candidates:
        print("No candidates found.")
        return

    print("List of All Candidates:")
    print("-" * 50)
    for candidate in candidates:
        print(f"ID: {candidate.id}")
        print(f"Name: {candidate.name}")
        print(f"Email: {candidate.email or 'N/A'}")
        print(f"Phone Number: {candidate.phone_num or 'N/A'}")
        print(f"Experience Years: {candidate.experience_years}")
        
        if candidate.certificates:
            certificates = ", ".join(cert.name for cert in candidate.certificates)
            print(f"Certificates: {certificates}")
        else:
            print("Certificates: N/A")

        if candidate.extra_qualifications:
            qualifications = ", ".join(qual.name for qual in candidate.extra_qualifications)
            print(f"Qualifications: {qualifications}")
        else:
            print("Qualifications: N/A")

        if candidate.skills:
            skills = ", ".join(skill.name for skill in candidate.skills)
            print(f"Skills: {skills}")
        else:
            print("Skills: N/A")

        print("-" * 50)

# print_all_candidates_interface()

def test():
    # List of dummy data to insert
    dummy_candidates = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone_num": "123456789",
            "experience_years": 5,
            "certificates": ["PMP", "AWS Certified Solutions Architect"],
            "qualifications": ["Bachelor's in Computer Science"],
            "skills": ["Python", "SQL", "Leadership"]
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone_num": "987654321",
            "experience_years": 3,
            "certificates": ["Certified Scrum Master"],
            "qualifications": ["Master's in Business Administration"],
            "skills": ["Agile", "Project Management"]
        },
        {
            "name": "Ali Ahmed",
            "email": "ali.ahmed@example.com",
            "phone_num": "5647382910",
            "experience_years": 7,
            "certificates": ["ITIL", "Azure Certified Developer"],
            "qualifications": ["Bachelor's in Information Technology"],
            "skills": ["Java", "Docker", "Kubernetes"]
        },
        {
            "name": "Sara Johnson",
            "email": "sara.johnson@example.com",
            "phone_num": "1122334455",
            "experience_years": 2,
            "certificates": ["Google Data Analytics"],
            "qualifications": ["Diploma in Data Science"],
            "skills": ["Excel", "Power BI", "Tableau"]
        },
        {
            "name": "Michael Brown",
            "email": None,  # No email provided
            "phone_num": "7788990011",
            "experience_years": 10,
            "certificates": ["CISSP", "Ethical Hacking"],
            "qualifications": ["Bachelor's in Cybersecurity"],
            "skills": ["Network Security", "Penetration Testing"]
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@example.com",
            "phone_num": None,  # No phone number provided
            "experience_years": 4,
            "certificates": None,  # No certificates
            "qualifications": ["Master's in Finance"],
            "skills": ["Financial Analysis", "Forecasting"]
        },
        {
            "name": "William Taylor",
            "email": "william.taylor@example.com",
            "phone_num": "4455667788",
            "experience_years": 6,
            "certificates": ["Microsoft Certified: Azure Solutions Architect"],
            "qualifications": ["Master's in Software Engineering"],
            "skills": ["C#", "ASP.NET", "Azure"]
        },
    ]

    # Insert each dummy candidate into the database
    for candidate_data in dummy_candidates:
        candidate = create_candidate_interface(
            name=candidate_data["name"],
            email=candidate_data.get("email"),
            phone_num=candidate_data.get("phone_num"),
            experience_years=candidate_data["experience_years"],
            certificates=candidate_data.get("certificates"),
            qualifications=candidate_data.get("qualifications"),
            skills=candidate_data.get("skills"),
        )
        if candidate:
            print(f"Inserted candidate: {candidate.name}")
        else:
            print(f"Failed to insert candidate: {candidate_data['name']}")

# Run the test function
if __name__ == "__main__":
    test()

