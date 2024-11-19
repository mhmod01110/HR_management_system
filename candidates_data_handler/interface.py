import os
import sys
# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from models import *
from candidate_manager import *


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

candidate_manager = CandidateManager(session)

# Use Case 1: Create a Candidate
def create_candidate_interface(
    name: str,
    email: Optional[str],
    phone_num: Optional[str],
    experience_years: int,
    certificates: Optional[List[int]] = None,
    qualifications: Optional[List[int]] = None,
    skills: Optional[List[int]] = None,
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


# Use Case 4: Update Candidate by ID
def update_candidate_interface(
    candidate_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone_num: Optional[str] = None,
    experience_years: Optional[int] = None,
    certificates: Optional[List[int]] = None,
    qualifications: Optional[List[int]] = None,
    skills: Optional[List[int]] = None,
):
    try:
        candidate = candidate_manager.update_by_id(
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

print_all_candidates_interface()