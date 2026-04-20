# Assignment 13 – JWT Authentication with Playwright E2E Testing

##  Overview

This project implements a full-stack FastAPI application with:

- JWT-based authentication (register/login)
- Front-end pages for user interaction
- Playwright end-to-end (E2E) testing
- Docker-based deployment
- CI/CD pipeline using GitHub Actions

---

##  Features

###  Authentication
- User registration (`/auth/register`)
- User login (`/auth/login`)
- Secure password hashing
- JWT token generation (access + refresh tokens)
- Token storage in browser (localStorage)

---

###  Front-End
- Register page (`/register`)
- Login page (`/login`)
- Client-side validation:
  - Email format
  - Password strength (uppercase, lowercase, number, special character)
- Displays success and error messages
- Redirects after successful login/registration

---

###  Testing

#### Playwright E2E Tests
Located in: tests/e2e/test_auth_ui.py


Covers:
-  Successful registration
-  Successful login
-  Invalid login (wrong password)
-  Weak password validation

---

###  CI/CD Pipeline

GitHub Actions workflow:
- Spins up PostgreSQL database
- Runs pytest and Playwright tests
- Builds Docker image
- Pushes to Docker Hub (if tests pass)

---

##  Running the Application

### 1. Start the app

```bash
docker compose up --build

### 2. Access the app
Home: http://localhost:8000
Register: http://localhost:8000/register
Login: http://localhost:8000/login
pgAdmin: http://localhost:5050

-> Running Tests
Activate virtual environment:

source venv/bin/activate

Install dependencies:
pip install -r requirements.txt 

Install Playwright browsers:
playwright install

Run E2E tests:
pytest tests/e2e/test_auth_ui.py

JWT Handling:
Access token stored in:
localStorage.access_token

Refresh token stored in:
localStorage.refresh_token

Docker Hub:
Docker image is pushed automatically:
https://hub.docker.com/r/gghanem07/assignment13

Screenshots Included:
- Playwright tests passing
- GitHub Actions success
- Register page working
- ogin page working
- Invalid login example
- Weak password validation example