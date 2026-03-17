# Online Loan Application Platform

This project implements an online loan application platform, allowing users to submit personal loan applications and loan officers to review and manage them. The platform is built with a React frontend and a FastAPI (Python) backend, utilizing PostgreSQL as the database.

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Future Enhancements](#future-enhancements)

## Architecture

The application follows a microservices-inspired architecture with a clear separation between the frontend and backend:

- **Frontend:** Developed with React, providing a user-friendly interface for loan applicants and a dashboard for loan officers.
- **Backend:** Built with FastAPI (Python), exposing RESTful APIs for application submission, retrieval, and review. It interacts with a PostgreSQL database.
- **Database:** PostgreSQL is used for secure storage of all application data.

## Features

### For Loan Applicants:
- Submit personal, financial, bank, loan, and legal information through an online form.
- View the status of their submitted loan applications (future).

### For Loan Officers:
- View a dashboard of pending loan applications.
- Review detailed information for each application.
- Manually approve or reject loan applications.

## Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose (recommended for easy setup)
- Python 3.9+
- Node.js (LTS version) and npm
- PostgreSQL (if not using Docker Compose for the database)

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `backend` directory based on `.env.example` and fill in your PostgreSQL database connection string and JWT secret key.
    ```
    DATABASE_URL="postgresql://user:password@localhost:5432/loandb"
    SECRET_KEY="your-super-secret-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    Replace `user`, `password`, `localhost:5432`, `loandb` with your PostgreSQL credentials and database name. Replace `your-super-secret-key` with a strong, random string.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Create a `.env` file in the `frontend` directory based on `.env.example`.
    ```
    REACT_APP_API_URL=http://localhost:8000
    ```
    Adjust the `REACT_APP_API_URL` if your backend is running on a different host or port.

## Running the Application

### Using Docker Compose (Recommended)

1.  Create a `docker-compose.yml` file in the root directory of the project (next to `frontend` and `backend` folders) with the following content:
    ```yaml
    version: '3.8'

    services:
      db:
        image: postgres:13
        environment:
          POSTGRES_DB: loandb
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        ports:
          - "5432:5432"
        volumes:
          - db_data:/var/lib/postgresql/data

      backend:
        build: ./backend
        ports:
          - "8000:8000"
        environment:
          DATABASE_URL: postgresql://user:password@db:5432/loandb
          SECRET_KEY: your-super-secret-key # Use a strong, random key
          ALGORITHM: HS256
          ACCESS_TOKEN_EXPIRE_MINUTES: 30
        depends_on:
          - db

      frontend:
        build: ./frontend
        ports:
          - "3000:80"
        environment:
          REACT_APP_API_URL: http://localhost:8000
        depends_on:
          - backend

    volumes:
      db_data:
    ```
    **Important:** Replace `your-super-secret-key` with the same strong, random key you used in the backend's `.env` file.

2.  From the root directory, run:
    ```bash
    docker-compose up --build
    ```
    The frontend will be accessible at `http://localhost:3000` and the backend API at `http://localhost:8000`.

### Manual Setup (Without Docker Compose)

#### Start PostgreSQL Database
Ensure your PostgreSQL database is running and accessible with the credentials provided in `backend/.env`.

#### Start Backend
1.  Navigate to the `backend` directory.
2.  Activate your virtual environment.
3.  Run the FastAPI application:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend API will be available at `http://localhost:8000`.

#### Start Frontend
1.  Navigate to the `frontend` directory.
2.  Run the React development server:
    ```bash
    npm start
    ```
    The frontend application will be available at `http://localhost:3000`.

## API Endpoints

The backend API provides the following endpoints (refer to `backend/app/main.py` for full details):

-   `POST /token`: Authenticate and get JWT token.
-   `POST /applicants/`: Register a new loan applicant.
-   `GET /applicants/me/`: Get current applicant's details (requires authentication).
-   `POST /loan-applications/`: Submit a new loan application (requires applicant authentication).
-   `GET /loan-applications/{application_id}`: Get a specific loan application by ID (requires applicant authentication for their own applications).
-   `POST /loan-officers/`: Register a new loan officer.
-   `GET /loan-officers/me/`: Get current loan officer's details (requires authentication).
-   `GET /loan-applications/pending/`: Get all pending loan applications (requires loan officer authentication).
-   `PUT /loan-applications/{application_id}/review`: Review and update the status of a loan application (requires loan officer authentication).

## Future Enhancements

Based on the HLD, several enhancements are planned for future iterations:

-   Integration with Credit Bureaus for automated credit checks.
-   Integration with Identity Verification Services (KYC).
-   Automated Decisioning Engine for loan approvals.
-   Notification Service (email/SMS) for application status updates.
-   Document Upload functionality.
-   Native mobile applications.
-   More robust user authentication and authorization (e.g., MFA).
