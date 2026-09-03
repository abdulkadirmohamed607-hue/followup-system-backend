# FollowUp System Backend

Django REST API backend for the FollowUp System.

## Overview

The FollowUp System is a patient and visitor management system designed to help manage patients, visitors, user accounts, and hospital visit records.

This repository contains the backend API built with Django and Django REST Framework.

## Technologies

* Python 3.13+
* Django 6.1.1
* Django REST Framework
* PostgreSQL
* Simple JWT Authentication
* CORS

## Main Features

* User authentication
* JWT-based authentication
* User and role management
* Admin and User roles
* Patient management
* Visitor management
* Visit session management
* Password change functionality
* Password reset by administrator
* RESTful API

## User Roles

### Admin

Administrators can:

* Manage system users
* Manage patients
* Manage visitors
* View reports
* Reset user passwords
* Manage user roles

### User

Regular users can:

* View and manage patients
* Record visitors
* Manage visitor check-in information

## Visit Sessions

The system supports three visitor sessions:

* Morning
* Day
* Evening

Visitor limits:

* Morning: 2 visitors
* Day: 2 visitors
* Evening: 3 visitors

## Authentication API

Main authentication endpoints:

```text
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/auth/change-password/
GET  /api/auth/me/
```

## User Management API

```text
GET    /api/auth/users/
POST   /api/auth/users/
GET    /api/auth/users/{id}/
PUT    /api/auth/users/{id}/
PATCH  /api/auth/users/{id}/
DELETE /api/auth/users/{id}/
POST   /api/auth/users/{id}/reset-password/
```

## Project Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Database

The backend uses PostgreSQL for data storage.

Database configuration should be provided through environment variables and should not be committed to GitHub.

## Frontend

The frontend of the FollowUp System is built separately using Angular.

## Development

This project is currently under active development.

---

**FollowUp System**
Patient and Visitor Management System
# FollowUp System Backend

Django REST API backend for the FollowUp System.

## Overview

The FollowUp System is a patient and visitor management system designed to help manage patients, visitors, user accounts, and hospital visit records.

This repository contains the backend API built with Django and Django REST Framework.

## Technologies

* Python 3.13+
* Django 6.1.1
* Django REST Framework
* PostgreSQL
* Simple JWT Authentication
* CORS

## Main Features

* User authentication
* JWT-based authentication
* User and role management
* Admin and User roles
* Patient management
* Visitor management
* Visit session management
* Password change functionality
* Password reset by administrator
* RESTful API

## User Roles

### Admin

Administrators can:

* Manage system users
* Manage patients
* Manage visitors
* View reports
* Reset user passwords
* Manage user roles

### User

Regular users can:

* View and manage patients
* Record visitors
* Manage visitor check-in information

## Visit Sessions

The system supports three visitor sessions:

* Morning
* Day
* Evening

Visitor limits:

* Morning: 2 visitors
* Day: 2 visitors
* Evening: 3 visitors

## Authentication API

Main authentication endpoints:

```text
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/auth/change-password/
GET  /api/auth/me/
```

## User Management API

```text
GET    /api/auth/users/
POST   /api/auth/users/
GET    /api/auth/users/{id}/
PUT    /api/auth/users/{id}/
PATCH  /api/auth/users/{id}/
DELETE /api/auth/users/{id}/
POST   /api/auth/users/{id}/reset-password/
```

## Project Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Database

The backend uses PostgreSQL for data storage.

Database configuration should be provided through environment variables and should not be committed to GitHub.

## Frontend

The frontend of the FollowUp System is built separately using Angular.

## Development

This project is currently under active development.

---

**FollowUp System**
Patient and Visitor Management System
# FollowUp System Backend

Django REST API backend for the FollowUp System.

## Overview

The FollowUp System is a patient and visitor management system designed to help manage patients, visitors, user accounts, and hospital visit records.

This repository contains the backend API built with Django and Django REST Framework.

## Technologies

* Python 3.13+
* Django 6.1.1
* Django REST Framework
* PostgreSQL
* Simple JWT Authentication
* CORS

## Main Features

* User authentication
* JWT-based authentication
* User and role management
* Admin and User roles
* Patient management
* Visitor management
* Visit session management
* Password change functionality
* Password reset by administrator
* RESTful API

## User Roles

### Admin

Administrators can:

* Manage system users
* Manage patients
* Manage visitors
* View reports
* Reset user passwords
* Manage user roles

### User

Regular users can:

* View and manage patients
* Record visitors
* Manage visitor check-in information

## Visit Sessions

The system supports three visitor sessions:

* Morning
* Day
* Evening

Visitor limits:

* Morning: 2 visitors
* Day: 2 visitors
* Evening: 3 visitors

## Authentication API

Main authentication endpoints:

```text
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/auth/change-password/
GET  /api/auth/me/
```

## User Management API

```text
GET    /api/auth/users/
POST   /api/auth/users/
GET    /api/auth/users/{id}/
PUT    /api/auth/users/{id}/
PATCH  /api/auth/users/{id}/
DELETE /api/auth/users/{id}/
POST   /api/auth/users/{id}/reset-password/
```

## Project Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Database

The backend uses PostgreSQL for data storage.

Database configuration should be provided through environment variables and should not be committed to GitHub.

## Frontend

The frontend of the FollowUp System is built separately using Angular.

## Development

This project is currently under active development.

---

**FollowUp System**
Patient and Visitor Management System
