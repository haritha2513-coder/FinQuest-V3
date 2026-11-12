# FinQuest V3 – Pastel Financial Literacy Dashboard

FinQuest is a responsive, Flask-based financial learning dashboard with a soft pastel piggy-bank theme. It helps students and beginners learn money management through short lessons, quizzes, a budget planner, and a spending tracker, all in one place.

**Live demo:** https://finquest-v3-1.onrender.com

## Features

- **Learning path:** Six finance modules with lesson content
- **Gamified progress:** Module completion, XP rewards, levels, and progress tracking
- **Daily quiz:** Six questions a day, with answer explanations and XP rewards
- **Budget planner:** An interactive monthly budget tool
- **Savings goal jar:** Set and track a savings goal (saved in the browser's local storage)
- **Spending tracker:** Log expenses, stored in a local SQLite database
- **Money learning coach:** A rule-based assistant that answers general money questions
- **Multilingual navigation:** English, Tamil, and Hindi language selector (the welcome label changes; lesson content is currently in English)
- **Responsive design:** Works on desktop and mobile

## Tech Stack

- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render, served with Gunicorn

## Project Structure
finquest/
├── app.py # Flask routes and database logic
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # Main page
└── static/
├── css/style.css # Styling
└── js/app.js # Frontend logic
## AUTHOR
Built by *** Binary Bytes*** for the Threws Odessey 2026 hackhathon
