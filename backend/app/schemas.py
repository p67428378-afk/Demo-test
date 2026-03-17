from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class ApplicantBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    address: str

class ApplicantCreate(ApplicantBase):
    pass

class Applicant(ApplicantBase):
    id: int

    class Config:
        from_attributes = True

class LoanApplicationBase(BaseModel):
    loan_amount: float
    loan_tenure: int
    financial_details: str
    bank_name: str
    account_number: str
    ifsc_swift_code: str
    legal_consent: bool

class LoanApplicationCreate(LoanApplicationBase):
    applicant_id: int

class LoanApplicationUpdate(BaseModel):
    status: Optional[str] = None
    decision: Optional[str] = None # For loan officer decision
    comments: Optional[str] = None # For loan officer comments

class LoanApplication(LoanApplicationBase):
    id: int
    applicant_id: int
    application_date: datetime
    status: str
    legal_consent_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoanOfficerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str = "Loan Officer"

class LoanOfficerCreate(LoanOfficerBase):
    password: str

class LoanOfficer(LoanOfficerBase):
    id: int

    class Config:
        from_attributes = True

class ApplicationReviewBase(BaseModel):
    application_id: int
    officer_id: int
    decision: str
    comments: Optional[str] = None

class ApplicationReviewCreate(ApplicationReviewBase):
    pass

class ApplicationReview(ApplicationReviewBase):
    id: int
    review_date: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
