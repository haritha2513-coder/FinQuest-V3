from flask import Flask, render_template, request, jsonify
import sqlite3, os, random
from datetime import date

app = Flask(__name__)
DB_PATH = os.path.join(app.root_path, "data", "finquest.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

MODULES = [
    {"id":"money-basics","title":"Money Mindset","category":"Foundations","level":"Beginner","minutes":12,"icon":"🌱","color":"mint","description":"Understand money, needs vs wants, and smart everyday choices.","lessons":[("What is money?","Money is a tool for exchanging value. It helps us buy goods, pay for services and plan for the future."),("Needs vs wants","Needs are essentials such as food and shelter. Wants make life enjoyable, but should fit your budget."),("SMART goals","Make goals Specific, Measurable, Achievable, Relevant and Time-bound.") ]},
    {"id":"budgeting","title":"Budget Like a Boss","category":"Budgeting","level":"Beginner","minutes":18,"icon":"🐷","color":"peach","description":"Build a simple budget and make every rupee count.","lessons":[("The 50/30/20 idea","A popular starting point is 50% needs, 30% wants and 20% savings or debt repayment. Adjust it to your reality."),("Track your spending","Record what you spend for a week. Small purchases add up, and awareness helps you make better choices."),("Build your first budget","List income, fixed costs, flexible costs and savings. Make sure your plan does not spend more than you earn.") ]},
    {"id":"saving","title":"Savings Superpower","category":"Saving","level":"Beginner","minutes":15,"icon":"🪙","color":"lavender","description":"Create an emergency fund and turn small habits into big wins.","lessons":[("Pay yourself first","Move a planned amount into savings when you receive money, rather than waiting to see what is left."),("Emergency fund","An emergency fund is money set aside for unexpected costs. Start small and build it steadily."),("Compound growth","Compounding means earning returns on both your original amount and earlier returns. Time can make a big difference.") ]},
    {"id":"credit","title":"Credit Confidence","category":"Credit","level":"Intermediate","minutes":20,"icon":"💳","color":"blue","description":"Learn how borrowing, interest and repayment work.","lessons":[("Credit basics","Credit lets you borrow now and repay later. It is useful when managed carefully, but borrowing has a cost."),("Understand interest","Interest is the cost of borrowing or the reward for saving. Compare rates and fees before deciding."),("Healthy credit habits","Pay on time, borrow only what you can repay and check statements for unfamiliar activity.") ]},
    {"id":"investing","title":"Investing Garden","category":"Investing","level":"Intermediate","minutes":22,"icon":"🌷","color":"mint","description":"Explore risk, diversification and long-term investing concepts.","lessons":[("Risk and return","Higher potential returns usually come with higher risk. Your time horizon and comfort with risk matter."),("Diversification","Spreading investments across different assets can reduce the impact of one investment performing poorly."),("Start with learning","Understand fees, goals, time horizon and risk before investing. This course is educational, not personal financial advice.") ]},
    {"id":"safety","title":"Digital Money Safety","category":"Safety","level":"Beginner","minutes":10,"icon":"🔐","color":"peach","description":"Spot scams and protect your accounts and payments.","lessons":[("Pause before you pay","Be suspicious of urgent requests, unexpected prizes and links asking for passwords or OTPs."),("Protect your accounts","Use unique passwords, enable two-factor authentication and never share an OTP or PIN."),("Verify first","Contact banks and services using their official app or website, not details in a suspicious message.") ]}
]

QUIZ = [
    {"q":"Which is the best example of a need?","opts":["A new gaming console","Basic groceries","A designer bag","A concert ticket"],"a":1,"why":"Food is an essential need. The other choices are generally wants."},
    {"q":"In a 50/30/20 budget, what does 20% commonly represent?","opts":["Entertainment","Housing","Savings and debt repayment","Shopping"],"a":2,"why":"The 20% category is commonly used for savings and debt repayment."},
    {"q":"What is an emergency fund for?","opts":["Planned holidays","Unexpected expenses","Daily coffee","Luxury shopping"],"a":1,"why":"It helps cover unexpected costs such as urgent repairs or a sudden loss of income."},
    {"q":"What does diversification mean?","opts":["Putting everything in one asset","Spreading investments","Avoiding all savings","Borrowing more"],"a":1,"why":"Diversification spreads risk across different investments."},
    {"q":"Should you share an OTP with someone who calls claiming to be from your bank?","opts":["Yes, if they sound official","Only at night","Never","Only for large payments"],"a":2,"why":"Never share an OTP, PIN or password. Contact your bank through official channels."},
    {"q":"What is compound growth?","opts":["Returns earning further returns","A monthly bill","A type of loan","A shopping discount"],"a":0,"why":"Compounding means returns can build on both your original amount and earlier returns."}
]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK(id=1), name TEXT DEFAULT 'Money Explorer',
            xp INTEGER DEFAULT 0, streak INTEGER DEFAULT 1, last_quiz TEXT DEFAULT '',
            quiz_score INTEGER DEFAULT 0, completed TEXT DEFAULT ''
        )""")
        con.execute("INSERT OR IGNORE INTO profile (id) VALUES (1)")
        con.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
            category TEXT NOT NULL, amount REAL NOT NULL, created TEXT NOT NULL
        )""")
init_db()

def state():
    with db() as con:
        p = dict(con.execute("SELECT * FROM profile WHERE id=1").fetchone())
        expenses = [dict(x) for x in con.execute("SELECT * FROM expenses ORDER BY id DESC LIMIT 12")]
    completed = [x for x in p["completed"].split(",") if x]
    p["completed_modules"] = completed
    p["modules"] = MODULES
    p["expenses"] = expenses
    p["total_spent"] = round(sum(x["amount"] for x in expenses), 2)
    p.pop("completed", None)
    return p

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/state")
def api_state():
    return jsonify(state())

@app.post("/api/profile")
def profile():
    name = (request.json or {}).get("name", "Money Explorer").strip()[:40] or "Money Explorer"
    with db() as con:
        con.execute("UPDATE profile SET name=? WHERE id=1", (name,))
    return jsonify(state())

@app.post("/api/complete")
def complete():
    mid = (request.json or {}).get("module_id")
    if mid not in [m["id"] for m in MODULES]:
        return jsonify({"error":"Unknown module"}), 400
    with db() as con:
        p = con.execute("SELECT completed FROM profile WHERE id=1").fetchone()
        done = [x for x in p["completed"].split(",") if x]
        if mid not in done:
            done.append(mid)
            con.execute("UPDATE profile SET completed=?, xp=xp+50 WHERE id=1", (",".join(done),))
    return jsonify(state())

@app.post("/api/quiz")
def quiz_submit():
    data = request.json or {}
    answers = data.get("answers", [])
    today = date.today().isoformat()
    score = sum(1 for i, q in enumerate(QUIZ) if i < len(answers) and answers[i] == q["a"])
    with db() as con:
        p = con.execute("SELECT last_quiz FROM profile WHERE id=1").fetchone()
        reward = 0 if p["last_quiz"] == today else score * 10 + 10
        con.execute("UPDATE profile SET xp=xp+?, last_quiz=?, quiz_score=? WHERE id=1",
                    (reward, today, score))
    return jsonify({"score":score, "total":len(QUIZ), "xp_earned":reward,
                    "review":[{"answer":q["a"],"why":q["why"]} for q in QUIZ], "state":state()})

@app.get("/api/quiz")
def quiz_get():
    return jsonify([{ "q":q["q"], "opts":q["opts"] } for q in QUIZ])

@app.post("/api/expenses")
def add_expense():
    data = request.json or {}
    title = str(data.get("title","")).strip()[:60]
    category = str(data.get("category","Other"))[:30]
    try: amount = float(data.get("amount",0))
    except (TypeError, ValueError): amount = 0
    if not title or amount <= 0 or amount > 100000000:
        return jsonify({"error":"Enter a description and an amount greater than zero."}), 400
    with db() as con:
        con.execute("INSERT INTO expenses(title,category,amount,created) VALUES(?,?,?,?)",
                    (title, category, amount, date.today().isoformat()))
    return jsonify(state())

@app.delete("/api/expenses/<int:eid>")
def delete_expense(eid):
    with db() as con:
        con.execute("DELETE FROM expenses WHERE id=?", (eid,))
    return jsonify(state())

@app.post("/api/coach")
def coach():
    question = str((request.json or {}).get("question","")).strip()
    if not question:
        return jsonify({"answer":"Type a money question and I’ll help you think it through."})
    q = question.lower()
    if any(w in q for w in ["budget","spend","expense"]):
        answer = "Try this: write down your monthly income, list essential costs first, set a realistic savings target, then give every remaining rupee a purpose. Track spending for a week and adjust without judging yourself."
    elif any(w in q for w in ["save","saving","emergency"]):
        answer = "Start with a small automatic amount you can repeat. Keep emergency savings separate from everyday spending, set a clear target, and increase the amount when your budget allows."
    elif any(w in q for w in ["invest","stock","share","mutual"]):
        answer = "Before investing, learn about risk, diversification, fees and your time horizon. Avoid investing money you may need soon, and be careful of guaranteed-return promises. This is general education, not investment advice."
    elif any(w in q for w in ["credit","loan","debt","interest"]):
        answer = "Compare the total repayment amount, interest rate, fees and repayment schedule before borrowing. Pay on time and avoid taking new debt to cover old debt unless you fully understand the consequences."
    elif any(w in q for w in ["scam","otp","fraud","safe"]):
        answer = "Never share your OTP, PIN or password. Do not click unexpected payment links. Verify requests through the official bank app or number, and report suspicious transactions immediately."
    else:
        answer = "A good money decision starts with a goal, the full cost, the risks and whether it fits your budget. Tell me whether your question is about budgeting, saving, credit, investing or online safety for a more focused explanation."
    return jsonify({"answer":answer})

if __name__ == "__main__":
    app.run(debug=True)
