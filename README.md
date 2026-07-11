# MeetMind

A Meeting Notes Organizer that extracts action items, assigns team members, detects due dates, and saves everything to the cloud—without requiring perfectly formatted text.

---

## Project Overview

| Category | Details |
| :--- | :--- |
| **Project Name** | MeetMind |
| **Domain** | Productivity & Task Automation |
| **Type** | Full-stack Web Application + REST API |
| **Status** | ✅ Complete |

MeetMind understands messy sentences like *"meeting with siddhi on tuesday"* or *"Project submission - 7 July"* and converts them into structured, trackable tasks.

---

## Features

- Upload messy meeting notes via Django web form
- Smart extraction using Regex + keyword detection (does **not** require "Action:")
- Auto-assigns tasks to team members found in sentences
- Parses dates like "tomorrow", "tuesday", "7 July" → `YYYY-MM-DD`
- Stores meetings and tasks in MongoDB Atlas
- Background thread checks for pending/overdue tasks every 10 seconds
- REST API endpoints (`/api/pending/`, `/api/meetings/`) for Slack integration
- One-click CSV export for Excel
- Meeting dashboard to view all stored meetings

---

## Tech Stack

- Python 3, Django 6.0, Django REST Framework
- MongoDB Atlas (PyMongo)
- Regular Expressions (Regex)
- Python Threading
- python-dotenv

---

## Project Structure

```
meetmind/
├── meetmind_web/            # Django project settings
│   ├── settings.py
│   └── urls.py
├── webapp/                  # Django app
│   ├── templates/           # HTML pages
│   ├── views.py             # Web logic + CSV export
│   ├── api_views.py         # DRF API endpoints
│   ├── serializers.py       # JSON serializers
│   ├── forms.py             # Django form definition
│   └── urls.py              # App URL routes
├── models.py                # ActionItem OOP class
├── extractor.py             # Regex parsing logic
├── database.py              # MongoDB CRUD operations
├── reminder.py              # Threading background worker
├── main.py                  # Launch script for reminders
├── export.py                # CSV export utility
├── .env.example             # Environment template
└── manage.py                # Django CLI
```

---

## How to Run

**1. Setup virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

**2. Configure MongoDB:**
Create a `.env` file with:
```
MONGO_URI="your_mongodb_atlas_uri"
```

**3. Run the web server:**
```bash
python manage.py runserver
```
Open `http://127.0.0.1:8000/`

**4. (Optional) Start background reminders:**
```bash
python main.py
```

---

## API Endpoints

| Endpoint | Description |
| :--- | :--- |
| `/api/pending/` | JSON list of all pending tasks |
| `/api/meetings/` | JSON list of all meetings |

---

## Sample Input → Output

**Input:**
```
Project submission - 7 July
meeting with siddhi on tuesday
```

**Output:**

| Description | Assignee | Due Date |
| :--- | :--- | :--- |
| Project submission | Unassigned | 2026-07-07 |
| meeting with siddhi | Siddhi | 2026-07-09 |

---

## Step-by-Step Progress (9 Tasks)

| Step | Task | File | Status |
| :--- | :--- | :--- | :--- |
| 1 | Django upload form | `webapp/forms.py`, `views.py` | ✅ |
| 2 | Regex extraction | `extractor.py` | ✅ |
| 3 | Auto-assignment | `extractor.py` | ✅ |
| 4 | MongoDB storage | `database.py` | ✅ |
| 5 | Completion status | `models.py` | ✅ |
| 6 | Multithreading | `reminder.py` | ✅ |
| 7 | Background reminders | `reminder.py` | ✅ |
| 8 | DRF API | `api_views.py`, `serializers.py` | ✅ |
| 9 | CSV export | `views.py` (`export_csv`) | ✅ |

---

Done!!
