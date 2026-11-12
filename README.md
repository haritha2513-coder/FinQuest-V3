# FinQuest V3 — Pastel Financial Literacy Dashboard

A Flask-based, responsive financial learning dashboard with a soft pastel piggy-bank theme.

## Features
- Learning path with six finance modules and lesson content
- Module completion, XP rewards, levels and progress tracking
- Daily six-question quiz with answer explanations and XP
- Interactive monthly budget planner
- Savings goal jar (saved in browser local storage)
- Spending tracker backed by SQLite
- Rule-based money learning coach
- English, Tamil and Hindi language selector (the navigation welcome label changes; lesson content is currently English)
- Responsive desktop and mobile layout
- SQLite database created automatically in `data/finquest.db`

## Run on Windows

1. Extract the ZIP file.
2. Open the extracted `finquest_v3` folder.
3. Click the folder address bar in File Explorer, type `cmd`, and press Enter.
4. Run these commands one by one:

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

5. Keep that Command Prompt window open.
6. Open Chrome and visit:

http://127.0.0.1:5000

## Stop the dashboard
Press `CTRL + C` in the Command Prompt.

## Important
- This is a local development project. It is not deployed publicly.
- Your learning progress and spending entries are stored in the local SQLite database in `data/finquest.db`.
- Savings goal values are stored in the browser's local storage.
- The coach provides general financial education, not personalized financial, tax or investment advice.
- Do not enter real bank passwords, card numbers, OTPs or other sensitive details.
- For a public launch, add authentication, CSRF protection, secure deployment settings, backups and a production WSGI server.
