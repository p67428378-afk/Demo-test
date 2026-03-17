from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from . import crud, models, schemas, auth
from .database import SessionLocal, engine, get_db

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the current applicant
def get_current_applicant(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    applicant = crud.get_applicant_by_email(db, email=email)
    if applicant is None:
        raise credentials_exception
    return applicant

# Dependency to get the current loan officer
def get_current_loan_officer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    loan_officer = crud.get_loan_officer_by_email(db, email=email)
    if loan_officer is None or loan_officer.role != "Loan Officer":
        raise credentials_exception
    return loan_officer


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_applicant_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password): # Assuming hashed_password will be added to Applicant model for simplicity
        user = crud.get_loan_officer_by_email(db, email=form_data.username)
        if not user or not auth.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role if hasattr(user, 'role') else 'Applicant'},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/applicants/", response_model=schemas.Applicant)
def create_applicant(applicant: schemas.ApplicantCreate, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant_by_email(db, email=applicant.email)
    if db_applicant:
        raise HTTPException(status_code=400, detail="Email already registered")
    # For simplicity, adding a placeholder hashed_password. In a real app, this would be part of registration.
    applicant_dict = applicant.model_dump()
    applicant_dict['hashed_password'] = auth.get_password_hash("default_password") # Placeholder
    return crud.create_applicant(db=db, applicant=schemas.ApplicantCreate(**applicant_dict))

@app.get("/applicants/me/", response_model=schemas.Applicant)
def read_applicant_me(current_applicant: schemas.Applicant = Depends(get_current_applicant)):
    return current_applicant

@app.post("/loan-applications/", response_model=schemas.LoanApplication)
def create_loan_application(application: schemas.LoanApplicationCreate, db: Session = Depends(get_db), current_applicant: schemas.Applicant = Depends(get_current_applicant)):
    if application.applicant_id != current_applicant.id:
        raise HTTPException(status_code=403, detail="Not authorized to create application for this applicant ID")
    return crud.create_loan_application(db=db, application=application)

@app.get("/loan-applications/{application_id}", response_model=schemas.LoanApplication)
def read_loan_application(application_id: int, db: Session = Depends(get_db), current_applicant: schemas.Applicant = Depends(get_current_applicant)):
    db_application = crud.get_loan_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Loan application not found")
    if db_application.applicant_id != current_applicant.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    return db_application

# Loan Officer Endpoints
@app.post("/loan-officers/", response_model=schemas.LoanOfficer)
def create_loan_officer(officer: schemas.LoanOfficerCreate, db: Session = Depends(get_db)):
    db_officer = crud.get_loan_officer_by_email(db, email=officer.email)
    if db_officer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_loan_officer(db=db, officer=officer)

@app.get("/loan-officers/me/", response_model=schemas.LoanOfficer)
def read_loan_officer_me(current_loan_officer: schemas.LoanOfficer = Depends(get_current_loan_officer)):
    return current_loan_officer

@app.get("/loan-applications/pending/", response_model=List[schemas.LoanApplication])
def read_pending_loan_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_loan_officer: schemas.LoanOfficer = Depends(get_current_loan_officer)):
    applications = db.query(models.LoanApplication).filter(models.LoanApplication.status == "Pending").offset(skip).limit(limit).all()
    return applications

@app.put("/loan-applications/{application_id}/review", response_model=schemas.LoanApplication)
def review_loan_application(application_id: int, review_data: schemas.LoanApplicationUpdate, db: Session = Depends(get_db), current_loan_officer: schemas.LoanOfficer = Depends(get_current_loan_officer)):
    db_application = crud.get_loan_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Loan application not found")
    
    if review_data.status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'Approved' or 'Rejected'")

    db_application = crud.update_loan_application_status(db, application_id=application_id, status=review_data.status)
    
    # Create an application review entry
    review_create = schemas.ApplicationReviewCreate(
        application_id=application_id,
        officer_id=current_loan_officer.id,
        decision=review_data.status,
        comments=review_data.comments
    )
    crud.create_application_review(db, review=review_create)

    return db_application
