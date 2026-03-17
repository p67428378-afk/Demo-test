from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from .auth import get_password_hash

def get_applicant(db: Session, applicant_id: int):
    return db.query(models.Applicant).filter(models.Applicant.id == applicant_id).first()

def get_applicant_by_email(db: Session, email: str):
    return db.query(models.Applicant).filter(models.Applicant.email == email).first()

def create_applicant(db: Session, applicant: schemas.ApplicantCreate):
    db_applicant = models.Applicant(**applicant.model_dump())
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return db_applicant

def get_loan_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LoanApplication).offset(skip).limit(limit).all()

def get_loan_application(db: Session, application_id: int):
    return db.query(models.LoanApplication).filter(models.LoanApplication.id == application_id).first()

def create_loan_application(db: Session, application: schemas.LoanApplicationCreate):
    db_application = models.LoanApplication(**application.model_dump())
    db_application.application_date = datetime.now()
    if db_application.legal_consent:
        db_application.legal_consent_timestamp = datetime.now()
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def update_loan_application_status(db: Session, application_id: int, status: str):
    db_application = db.query(models.LoanApplication).filter(models.LoanApplication.id == application_id).first()
    if db_application:
        db_application.status = status
        db.commit()
        db.refresh(db_application)
    return db_application

def get_loan_officer(db: Session, officer_id: int):
    return db.query(models.LoanOfficer).filter(models.LoanOfficer.id == officer_id).first()

def get_loan_officer_by_email(db: Session, email: str):
    return db.query(models.LoanOfficer).filter(models.LoanOfficer.email == email).first()

def create_loan_officer(db: Session, officer: schemas.LoanOfficerCreate):
    hashed_password = get_password_hash(officer.password)
    db_officer = models.LoanOfficer(email=officer.email, hashed_password=hashed_password, first_name=officer.first_name, last_name=officer.last_name, role=officer.role)
    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)
    return db_officer

def create_application_review(db: Session, review: schemas.ApplicationReviewCreate):
    db_review = models.ApplicationReview(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
