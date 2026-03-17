from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    address = Column(String)
    hashed_password = Column(String) # Added for authentication

    applications = relationship("LoanApplication", back_populates="applicant")

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    loan_amount = Column(Float)
    loan_tenure = Column(Integer) # in months
    application_date = Column(DateTime, default=func.now())
    status = Column(String, default="Pending") # Pending, Approved, Rejected
    financial_details = Column(String) # JSON string or separate table in future
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_swift_code = Column(String)
    legal_consent = Column(Boolean, default=False)
    legal_consent_timestamp = Column(DateTime, nullable=True)

    applicant = relationship("Applicant", back_populates="applications")
    reviews = relationship("ApplicationReview", back_populates="loan_application")

class LoanOfficer(Base):
    __tablename__ = "loan_officers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="Loan Officer")
    hashed_password = Column(String) # For authentication

    reviews = relationship("ApplicationReview", back_populates="loan_officer")

class ApplicationReview(Base):
    __tablename__ = "application_reviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"))
    officer_id = Column(Integer, ForeignKey("loan_officers.id"))
    review_date = Column(DateTime, default=func.now())
    decision = Column(String) # Approved, Rejected
    comments = Column(String, nullable=True)

    loan_application = relationship("LoanApplication", back_populates="reviews")
    loan_officer = relationship("LoanOfficer", back_populates="reviews")
