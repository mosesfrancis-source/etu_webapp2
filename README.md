# ETU Mathematics Department Portal

A full-featured academic management system for the Department of Mathematics at Eastern Technical University of Sierra Leone (ETUSL). Built with Django and PostgreSQL, it provides separate portals for students, lecturers, the Head of Department, and administrators.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [Features](#features)
- [Data Models](#data-models)
- [URL Reference](#url-reference)
- [Access Control](#access-control)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Deployment (Render)](#deployment-render)

---

## Overview

The portal serves as the central hub for the Mathematics Department, handling:

- Student and lecturer registration (via PIN-gated system)
- Course registration and management
- Grade entry and GPA calculation
- Announcements, course materials, tutorials, and assignments
- Internal messaging between users
- Attendance tracking and exam scheduling
- Fee payment submission and verification
- Office hours and appointment booking

Public-facing pages (Home, About, News, Contact) are accessible without login. All academic data — courses, faculty, grades, materials, messages — requires authentication.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.x |
| Database | PostgreSQL (local) / `dj-database-url` (hosted) |
| Auth | Django's built-in auth + custom `User` model |
| Static files | WhiteNoise (`CompressedManifestStaticFilesStorage`) |
| Media storage | Local filesystem or Cloudinary (via `CLOUDINARY_URL`) |
| Frontend | Bootstrap 5.3, Bootstrap Icons 1.11, Inter font |
| Hosting | Render (configured via `RENDER_EXTERNAL_HOSTNAME`) |

---

## Project Structure

```
EtuSLapp/
└── myproject/
    ├── myproject/          # Django project config (settings, URLs, WSGI)
    ├── accounts/           # Auth, profiles, announcements, messaging, fees, etc.
    │   ├── models.py       # All non-course models
    │   ├── views.py        # Auth views, public pages, admin tools
    │   ├── portal_views.py # Student and lecturer portal section views
    │   ├── forms.py        # Registration and profile forms
    │   ├── context_processors.py  # Injects sidebar activity data globally
    │   └── templates/
    │       ├── base.html           # Site-wide layout (nav, sidebar, footer)
    │       ├── home.html / about.html / programs.html / faculty.html / ...
    │       └── accounts/           # Login, register, dashboard, portal templates
    ├── courses/            # Course catalogue, registration, grading
    │   ├── models.py       # Course, CourseRegistration, Grade
    │   ├── views.py        # Course CRUD, registration, grade entry
    │   └── templates/courses/
    └── static/             # CSS, images
```

---

## User Roles

There are four roles, set on the `User` model:

| Role | Description |
|---|---|
| `student` | Registers for courses, views grades, submits assignments and fees |
| `lecturer` | Manages their assigned courses, grades students, posts materials |
| `hod` | All lecturer permissions plus full course management (add/edit/delete/assign) |
| `admin` | Manages users, generates registration PINs, verifies fee payments |

Superusers (`is_superuser=True`) are treated as admins throughout the application.

---

## Features

### Public (no login required)
- **Home** — Department overview with live counts of students, staff, and active courses
- **About** — Institutional information
- **News** — Department news
- **Contact** — Contact details

### Authentication
- **Student registration** — Open self-registration with username, email, and password
- **Lecturer/HOD registration** — PIN-gated; an admin must generate a PIN first
- **Login** — Accepts username or email address
- **Password reset** — Email-based reset flow (Django built-in)
- **Settings** — Change password or update profile picture and phone number

### Student Portal
- **Dashboard** — Summary of enrolled courses, recent activity, and upcoming deadlines
- **My Courses** — List of approved course registrations with lecturer details
- **My Registration** — Browse and register for available courses (filtered by year of study); drop courses not yet graded
- **My GPA** — Cumulative GPA and per-course grade breakdown
- **Grades** — Detailed grade view including component scores (coursework, assignments, tests, exams, practicals)
- **Announcements** — Department announcements targeted to all students, specific year levels, or specific courses
- **Materials** — Course materials uploaded by lecturers (notes, PDFs, slides, videos, links)
- **Assignments** — View published assignments and submit (file upload or text)
- **Discussions** — Course discussion threads with replies
- **Timetable** — Weekly class schedule
- **Appointments** — Request office-hour meetings with lecturers
- **Resources** — General department resources (past papers, forms, etc.)
- **Fee Payments** — Submit Orange Money payment receipts for admin verification

### Lecturer Portal
- **Dashboard** — Analytics overview (enrolled counts, submission stats, upcoming exams)
- **My Courses** — List of assigned courses; view enrolled students per course
- **Grade Management** — Enter and update component grades for each registered student
- **Assignments** — Create and publish assignments for enrolled students
- **Materials** — Upload course materials (files or external links)
- **Tutorials** — Post worked examples and practice exercises
- **Announcements** — Create targeted announcements
- **Messages** — Internal inbox and compose
- **Discussions** — Moderate and participate in course discussions
- **Attendance** — Mark student attendance per session
- **Tests / Exams** — Schedule quizzes, tests, midterms, and exams
- **Timetable** — View and manage weekly schedule
- **Office Hours** — Publish available office-hour slots; approve or decline student appointment requests
- **Analytics** — Grade distributions and engagement metrics

### HOD Portal
All lecturer features, plus:
- **Manage Courses** — View all courses with filtering by year and semester
- **Add / Edit / Delete Course** — Full CRUD for the course catalogue
- **Assign Lecturer** — Assign or re-assign a lecturer to any course

### Admin Portal
- **Manage Courses** — Same course management access as HOD
- **PIN Management** — Generate 8-character registration PINs tied to an email address and role
- **User Management** — List, search, edit, and delete all user accounts
- **Fee Payments** — Review, verify, or reject student payment submissions
- **Announcements / Resources / Messages** — Full access
- **Django Admin** — Full access at `/admin/`

---

## Data Models

### `accounts` app

| Model | Purpose |
|---|---|
| `User` | Extends `AbstractUser`; adds `role`, `profile_picture`, `phone` |
| `StudentProfile` | One-to-one with User; stores `student_id`, `year_of_study`, `date_of_birth` |
| `LecturerProfile` | One-to-one with User; stores `staff_id`, `specialization`, `position`, `office_number`, `bio`, etc. |
| `RegistrationPIN` | Single-use 8-char PIN linked to an email and role, generated by admins |
| `Announcement` | Targeted notices with audience filtering (all students, specific year levels, specific courses, staff only); supports scheduling |
| `Resource` | Department file uploads (notes, past papers, forms, etc.) |
| `Message` | Direct messages between users with thread support and file attachments |
| `ConversationThread` | Groups related messages; can be linked to a course |
| `CourseMaterial` | Course-specific files or links uploaded by lecturers |
| `Assignment` | Course assignment with due date, marks, and late-submission control |
| `AssignmentSubmission` | Student file or text submission for an assignment |
| `Tutorial` | Worked examples and practice exercises posted by lecturers |
| `Attendance` | Per-session attendance record (present / absent / late / excused) |
| `Discussion` | Course discussion thread; can reference an assignment |
| `DiscussionReply` | Reply to a discussion thread |
| `OfficeHour` | Recurring weekly availability slot for a lecturer |
| `AppointmentRequest` | Student request for a meeting during a lecturer's office hours |
| `Timetable` | Weekly class schedule entry (lecture, tutorial, practical, extra class) |
| `ExamSchedule` | Scheduled quiz, test, midterm, or exam for a course |
| `Notification` | In-app notifications for grades, messages, assignments, etc. |
| `FeePayment` | Student fee submission with Orange Money transaction ID and receipt image |

### `courses` app

| Model | Purpose |
|---|---|
| `Course` | Core catalogue entry: `code`, `name`, `credits`, `lecturer`, `semester`, `year_of_study`, `max_students`, `is_active` |
| `CourseRegistration` | Links a student to a course; status: `pending / approved / dropped / rejected` |
| `Grade` | One-to-one with `CourseRegistration`; stores component scores (coursework, assignments, tests, quizzes, exams, practicals, participation) and auto-calculates `total_score`, `letter_grade`, and `grade_point` |

GPA is computed by the `calculate_gpa(user)` function using credit-weighted grade points across all approved, graded registrations.

---

## URL Reference

### Public
| URL | View | Description |
|---|---|---|
| `/` | `home` | Homepage |
| `/about/` | `about` | About page |
| `/news/` | `news` | News |
| `/contact/` | `contact` | Contact |
| `/login/` | `login_view` | Login |
| `/logout/` | `logout_view` | Logout |
| `/register/` | `register` | Student registration |
| `/register/lecturer/` | `register_lecturer` | Lecturer registration (PIN required) |
| `/password-reset/` | — | Password reset flow |

### Authenticated only
| URL | View | Description |
|---|---|---|
| `/programs/` | `programs` | Full course catalogue by year/semester |
| `/faculty/` | `faculty` | Staff directory |
| `/students/` | `students` | Students page |
| `/dashboard/` | `dashboard` | Role-based dashboard redirect |
| `/settings/` | `settings` | Profile settings |

### Student
| URL | Description |
|---|---|
| `/courses/` | Available courses to register |
| `/courses/register/<id>/` | Register for a course |
| `/courses/drop/<id>/` | Drop a course |
| `/courses/my-courses/` | Enrolled courses |
| `/courses/grades/` | GPA and grade breakdown |
| `/portal/announcements/` | Student announcements |
| `/portal/materials/` | Course materials |
| `/portal/assignments/` | Assignments |
| `/portal/grades/` | Detailed grades |
| `/portal/discussions/` | Discussions |
| `/portal/appointments/` | Office-hour appointments |
| `/portal/timetable/` | Class timetable |
| `/fees/` | Fee payment submission |

### Lecturer / HOD
| URL | Description |
|---|---|
| `/lecturer/` | Lecturer dashboard |
| `/courses/teach/` | Assigned courses |
| `/courses/teach/<id>/students/` | Students in a course |
| `/courses/teach/grade/<id>/` | Grade a student |
| `/lecturer/grades/`, `/assignments/`, `/materials/`, etc. | Portal sections |

### HOD / Admin
| URL | Description |
|---|---|
| `/courses/manage/` | All courses (filterable) |
| `/courses/manage/add/` | Add a course |
| `/courses/manage/<id>/edit/` | Edit a course |
| `/courses/manage/<id>/delete/` | Delete a course |
| `/courses/manage/<id>/assign-lecturer/` | Assign a lecturer |
| `/portal/pins/` | PIN management |
| `/portal/users/` | User management |
| `/portal/users/<id>/edit/` | Edit a user |
| `/portal/users/<id>/delete/` | Delete a user |
| `/fees/<id>/review/` | Verify or reject a fee payment |

---

## Access Control

Every protected view uses `@login_required(login_url='login')`. Role enforcement is handled by two decorators:

- **`@role_required(*roles)`** (courses app) — redirects to dashboard if the user's role is not in the allowed list
- **`@_role_guard(roles)`** (accounts portal views) — same behaviour for portal section views

Role checks:
- Student pages require `role == 'student'`
- Lecturer pages require `role in ('lecturer', 'hod')`
- Course management requires `role in ('hod', 'admin')`
- Admin pages require `role == 'admin'` or `is_superuser`

The base template also conditionally renders sidebar navigation and the Programs / Faculty / Students nav links based on `request.user.is_authenticated`.

---

## Installation

**Prerequisites:** Python 3.10+, PostgreSQL

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd EtuSLapp/myproject

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database
createdb math_dept_weppApp_db2

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (admin account)
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to open the app. Log in with your superuser credentials and navigate to `/portal/pins/` to generate registration PINs for lecturers.

---

## Environment Variables

Create a `.env` file (or set these in your hosting environment):

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | insecure dev key | Django secret key — **must be changed in production** |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of allowed hostnames |
| `DATABASE_URL` | *(not set)* | Full database URL (used instead of individual DB vars when set) |
| `DB_NAME` | `math_dept_weppApp_db2` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | — | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `CLOUDINARY_URL` | *(not set)* | Cloudinary connection string for cloud media storage |
| `RENDER_EXTERNAL_HOSTNAME` | *(not set)* | Automatically set by Render; added to `ALLOWED_HOSTS` |

---

## Deployment (Render)

The project is pre-configured for [Render](https://render.com):

- `whitenoise` serves static files — no separate static file server needed
- `dj-database-url` parses a `DATABASE_URL` connection string
- `RENDER_EXTERNAL_HOSTNAME` is automatically added to `ALLOWED_HOSTS`
- `CLOUDINARY_URL` switches media storage to Cloudinary if set

Recommended Render build command:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:
```
gunicorn myproject.wsgi:application
```
