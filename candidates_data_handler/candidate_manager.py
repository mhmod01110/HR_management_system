import csv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional
from models import *

class CandidateManager:
    def __init__(self, session: Session):
        self.session = session

    def is_email_unique(self, email: str) -> bool:
        return self.session.query(Candidate).filter_by(email=email).first() is None

    def is_phone_num_unique(self, phone_num: str) -> bool:
        return self.session.query(Candidate).filter_by(phone_num=phone_num).first() is None
    
    def create_candidate(
        self, 
        name: str, 
        email: Optional[str], 
        phone_num: Optional[str], 
        experience_years: int,
        certificates: Optional[List[str]] = None,
        qualifications: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
    ) -> Candidate:
        if email and not self.is_email_unique(email):
            print("Email is already in use.")
            return
        if phone_num and not self.is_phone_num_unique(phone_num):
            print("Phone number is already in use.")
            return

        candidate = Candidate(
            name=name,
            email=email,
            phone_num=phone_num,
            experience_years=experience_years,
        )

        # Add certificates
        if certificates:
            candidate.certificates = [
                self.get_or_create(Certificate, name=cert_name) for cert_name in certificates
            ]

        # Add qualifications
        if qualifications:
            candidate.extra_qualifications = [
                self.get_or_create(Qualification, name=qual_name) for qual_name in qualifications
            ]

        # Add skills
        if skills:
            candidate.skills = [
                self.get_or_create(Skill, name=skill_name) for skill_name in skills
            ]

        self.session.add(candidate)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            print("Failed to create candidate due to integrity issues.")
        return candidate

    def get_or_create(self, model, **kwargs):
        """Fetch an object by attributes or create it if it doesn’t exist."""
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        instance = model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        return self.session.query(Candidate).get(candidate_id)

    def get_all(self) -> List[Candidate]:
        return self.session.query(Candidate).all()

    def edit_by_id(
        self, 
        candidate_id: int, 
        name: Optional[str] = None, 
        email: Optional[str] = None, 
        phone_num: Optional[str] = None, 
        experience_years: Optional[int] = None,
        certificates: Optional[List[str]] = None,
        qualifications: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
    ) -> Optional[Candidate]:
        candidate = self.get_by_id(candidate_id)
        if not candidate:
            print("Candidate not found.")
            return None

        if name:
            candidate.name = name
        if email:
            if email != candidate.email and not self.is_email_unique(email):
                print("Email is already in use.")
                return
            candidate.email = email
        if phone_num:
            if phone_num != candidate.phone_num and not self.is_phone_num_unique(phone_num):
                print("Phone number is already in use.")
                return
            candidate.phone_num = phone_num
        if experience_years is not None:
            candidate.experience_years = experience_years

        # edit certificates
        if certificates is not None:
            candidate.certificates = [
                self.get_or_create(Certificate, name=cert_name) for cert_name in certificates
            ]

        # edit qualifications
        if qualifications is not None:
            candidate.extra_qualifications = [
                self.get_or_create(Qualification, name=qual_name) for qual_name in qualifications
            ]

        # edit skills
        if skills is not None:
            candidate.skills = [
                self.get_or_create(Skill, name=skill_name) for skill_name in skills
            ]

        self.session.commit()
        return candidate


    def delete(self, candidate_id: int) -> bool:
        candidate = self.get_by_id(candidate_id)
        if not candidate:
            return False

        self.session.delete(candidate)
        self.session.commit()
        return True

    def export_to_csv(self, file_path: str) -> None:
        candidates = self.get_all()
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Header
            writer.writerow([
                "ID", "Name", "Email", "Phone Number", 
                "Experience Years", "Certificates", 
                "Qualifications", "Skills"
            ])
            for candidate in candidates:
                writer.writerow([
                    candidate.id,
                    candidate.name,
                    candidate.email,
                    candidate.phone_num,
                    candidate.experience_years,
                    ", ".join([cert.name for cert in candidate.certificates]) if candidate.certificates else "",
                    ", ".join([qual.name for qual in candidate.extra_qualifications]) if candidate.extra_qualifications else "",
                    ", ".join([skill.name for skill in candidate.skills]) if candidate.skills else "",
                ])
