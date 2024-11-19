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
        certificates: Optional[List[int]] = None,
        qualifications: Optional[List[int]] = None,
        skills: Optional[List[int]] = None,
    ) -> Candidate:
        if email and not self.is_email_unique(email):
            raise ValueError("Email is already in use.")
        if phone_num and not self.is_phone_num_unique(phone_num):
            raise ValueError("Phone number is already in use.")

        candidate = Candidate(
            name=name,
            email=email,
            phone_num=phone_num,
            experience_years=experience_years,
        )

        if certificates:
            candidate.certificates = self.session.query(Certificate).filter(Certificate.id.in_(certificates)).all()
        if qualifications:
            candidate.extra_qualifications = self.session.query(Qualification).filter(Qualification.id.in_(qualifications)).all()
        if skills:
            candidate.skills = self.session.query(Skill).filter(Skill.id.in_(skills)).all()

        self.session.add(candidate)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Failed to create candidate due to integrity issues.")
        return candidate

    def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        return self.session.query(Candidate).get(candidate_id)

    def get_all(self) -> List[Candidate]:
        return self.session.query(Candidate).all()

    def update_by_id(
        self, 
        candidate_id: int, 
        name: Optional[str] = None, 
        email: Optional[str] = None, 
        phone_num: Optional[str] = None, 
        experience_years: Optional[int] = None,
        certificates: Optional[List[int]] = None,
        qualifications: Optional[List[int]] = None,
        skills: Optional[List[int]] = None,
    ) -> Optional[Candidate]:
        candidate = self.get_by_id(candidate_id)
        if not candidate:
            return None

        if name:
            candidate.name = name
        if email:
            if email != candidate.email and not self.is_email_unique(email):
                raise ValueError("Email is already in use.")
            candidate.email = email
        if phone_num:
            if phone_num != candidate.phone_num and not self.is_phone_num_unique(phone_num):
                raise ValueError("Phone number is already in use.")
            candidate.phone_num = phone_num
        if experience_years is not None:
            candidate.experience_years = experience_years
        if certificates:
            candidate.certificates = self.session.query(Certificate).filter(Certificate.id.in_(certificates)).all()
        if qualifications:
            candidate.extra_qualifications = self.session.query(Qualification).filter(Qualification.id.in_(qualifications)).all()
        if skills:
            candidate.skills = self.session.query(Skill).filter(Skill.id.in_(skills)).all()

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
            writer.writerow(["ID", "Name", "Email", "Phone Number", "Experience Years"])
            for candidate in candidates:
                writer.writerow([
                    candidate.id, 
                    candidate.name, 
                    candidate.email, 
                    candidate.phone_num, 
                    candidate.experience_years,
                ])
