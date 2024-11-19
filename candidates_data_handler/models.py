from sqlalchemy import (
    Column, Integer, String, Table, ForeignKey, create_engine
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Association tables for many-to-many relationships
candidate_certificates = Table(
    "candidate_certificates",
    Base.metadata,
    Column("candidate_id", Integer, ForeignKey("candidates.id"), primary_key=True),
    Column("certificate_id", Integer, ForeignKey("certificates.id"), primary_key=True),
)

candidate_qualifications = Table(
    "candidate_qualifications",
    Base.metadata,
    Column("candidate_id", Integer, ForeignKey("candidates.id"), primary_key=True),
    Column("qualification_id", Integer, ForeignKey("qualifications.id"), primary_key=True),
)

candidate_skills = Table(
    "candidate_skills",
    Base.metadata,
    Column("candidate_id", Integer, ForeignKey("candidates.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)


# Main Candidate model
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone_num = Column(String(100), unique=True, nullable=True)
    experience_years = Column(Integer, nullable=False)

    # Relationships
    certificates = relationship(
        "Certificate",
        secondary=candidate_certificates,
        back_populates="candidates",
        cascade="all, delete",
    )
    extra_qualifications = relationship(
        "Qualification",
        secondary=candidate_qualifications,
        back_populates="candidates",
        cascade="all, delete",
    )
    skills = relationship(
        "Skill",
        secondary=candidate_skills,
        back_populates="candidates",
        cascade="all, delete",
    )


# Certificate model
class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    candidates = relationship(
        "Candidate",
        secondary=candidate_certificates,
        back_populates="certificates",
    )


# Qualification model
class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    candidates = relationship(
        "Candidate",
        secondary=candidate_qualifications,
        back_populates="extra_qualifications",
    )


# Skill model
class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    candidates = relationship(
        "Candidate",
        secondary=candidate_skills,
        back_populates="skills",
    )


# Database setup
DATABASE_URL = "sqlite:///candidates.db"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
