# Security Event Tracker
**Group 6 – CIS4930 SP26**

## Team Members
- **Vanessa Campoe** – **VAC23A** – Models / Data
- **Max Siska** – **MMS24I** – API / Analytics
- **Mateo Linares Figueroa** – **ML22BZ** – Views / Templates
- **Vivianna Loredo** – **VL22J** – Frontend / Documentation

## Project Description
Cybersecurity incidents have become one of the biggest real-world problems in modern computing. They can disrupt systems, expose sensitive information, and create serious consequences for both organizations and everyday users. For this project, our group built a Django web application that tracks and analyzes security events using cybersecurity attack data. The goal was to take the work from our earlier projects and turn it into a full website where users can browse records, manage entries, and view analytics through a clean and navigable interface.

## Original Dataset
- **Kaggle – Cyber Security Attacks**  
  **Link:** `https://www.kaggle.com/datasets/teamincribo/cyber-security-attacks`

## API Documentation
- **Open-Meteo Forecast API**  
  **Docs:** `https://open-meteo.com/en/docs`

## Application Features
- Homepage (`/`) with a short description of the project and navigation links
- Records list page (`/records/`) with pagination
- Detail view for a single security event (`/records/<pk>/`)
- Create view for adding a new security event (`/records/add/`)
- Update view for editing an existing record (`/records/<pk>/edit/`)
- Delete view with confirmation page (`/records/<pk>/delete/`)
- Analytics dashboard (`/analytics/`) with Chart.js charts and summary statistics
- Bootstrap 5 navbar, cards, tables, and form styling
- Custom CSS overrides in `static/css/style.css`
- Seed command to load the Project 1 CSV into the database
- Production-ready settings split into `base.py`, `dev.py`, and `prod.py`

## Research Questions Reused from Project 1
- Which attack categories appear most frequently in the dataset?
- How do threat score and packet length behave across the stored records?
- Is there a visible pattern in how actions taken relate to the security events in the dataset?

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd cis4930-sp26-django-project-group6
   ```

2. **Install dependencies**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Create a local `.env` file**

   In the project root, create a file named `.env` and add:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

4. **Apply migrations**
   ```bash
   python3 manage.py migrate
   ```

5. **Load the Project 1 CSV data**
   ```bash
   python3 manage.py seed_data
   ```

6. **Run the development server**
   ```bash
   python3 manage.py runserver
   ```

7. **Open the app in your browser**
   ```text
   http://127.0.0.1:8000/
   ```

## Screenshots

### Homepage
![Homepage](https://github.com/user-attachments/assets/ed23936d-6720-4f27-8ebd-e5106c3cbb92)

### Records List View
![Records List View](https://github.com/user-attachments/assets/f5520b7d-1d42-4dba-882e-ff3e664b5f77)

### Analytics Dashboard
![Analytics Dashboard 1](https://github.com/user-attachments/assets/2dc65383-442d-4177-a0a6-3aff287df3b6)

![Analytics Dashboard 2](https://github.com/user-attachments/assets/9230d3cd-53a7-4a86-9956-8c1ea8c9853f)

### Create Form
![Create Form](https://github.com/user-attachments/assets/25784bc4-6ff6-4c6c-958b-93805d73aba3)

## `manage.py check --deploy` Output

Command used:
```bash
DJANGO_SETTINGS_MODULE=config.settings.prod python3 manage.py check --deploy
```

Output:
```text
System check identified no issues (0 silenced).
```

## Team Organization Note
The work was split up by role so everything had a clear owner. The models/data side handled the database setup, migrations, and seeded data. The views/templates side handled the routing and CRUD pages. The API/analytics side handled the analytics logic and chart data. The frontend/documentation side focused on Bootstrap styling, custom CSS, deployment-readiness configuration, and the final README.

## Final Notes
This project combines work from our earlier data and API projects into one Django application that is fully navigable through a browser. The site supports CRUD operations, displays analytics based on stored records, and includes deployment-ready configuration files for submission.
