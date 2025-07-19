# Personal-Expense-Tracker
# 🧾 Personal Expense Tracker (CLI‑Based, Pipenv)

A cross‑platform command‑line application that lets you **log**, **categorise**, and **summarise** your day‑to‑day expenses.
Built with **Python 3.11+**, **SQLite**, **SQLAlchemy**, and **Click**, and packaged with **Pipenv** for painless environment management.

<img src="hhttps://github.com/kiarie27/Personal-Expense-Tracker-demo/main/demo.gif" width="720" alt="Animated CLI demo showing add, list, summary" />

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Add expense** | `add` command or interactive menu; takes date, category, amount, optional description |
| **List expenses** | Filter by category and/or date range; pretty table output |
| **Summary** | Totals per category, optionally for a single month and/or top‑N categories |
| **Interactive mode** | Full‑screen style menu (`pipenv run tracker`) for casual use |
| **Command mode** | Direct CLI scripts for automation or shell aliases |
| **SQLite + SQLAlchemy** | No external DB server needed, yet full ORM power |
| **Unit tests** | Pytest suite with separate in‑memory DB—safe to hack & extend |
| **Seed script** | One‑shot script populates demo data for screenshots & demos |

---

## 📂 Project Structure

```text
expense-tracker/
├── Pipfile               # Dependency & scripts definition
├── Pipfile.lock
├── README.md
├── tracker.py            # CLI entry point (Click group + menu)
├── db/
│   └── database.py       # Engine + Session factory
├── models/
│   └── expense.py        # Expense ORM model
├── commands/             # Each sub‑command in its own module
│   ├── add.py
│   ├── list.py
│   └── summary.py
├── tests/                # Pytest suites (TDD‑ready)
│   ├── conftest.py
│   ├── test_add.py
│   ├── test_list.py
│   └── test_summary.py
├── init_db.py            # Re‑creates DB & loads sample rows
└── expenses.db           # Auto‑created SQLite file (git‑ignored)
```

---

## 🚀 Quick Start

### 1  Clone & Install

```bash
git clone https://github.com/kiarie27/Personal-Expense-Tracker.git
cd expense-tracker

# Ensure you have Python ≥ 3.11 on PATH, then:
pip install --user pipenv
pipenv install --dev        # installs runtime + pytest
```

### 2  Initialise the Database (optional seed data)

```bash
pipenv run python init_db.py
# => 📂 Database initialised and seeded at expenses.db
```

> **What does `init_db.py` do?**
> • Creates the `expenses.db` file (if it doesn't exist).
> • Drops and recreates the `expenses` table.
> • Inserts five  demo expenses so `list` and `summary` have data to show.
>
> **Prefer to start empty?**
> Simply skip the script—running any tracker command will auto‑create an empty database on first launch.
>
> **Need demo data again later?**
> Re‑run:
>
> ```bash
> pipenv run python init_db.py
> ```


### 3  Run the App

**Interactive menu**

```bash
pipenv run tracker
```

You’ll see:

```text
===== Personal Expense Tracker =====
1) Add expense
2) List expenses
3) Summary
4) Exit
```

**Command mode**

| Command | Example |
|---------|---------|
| Add      | `pipenv run add-expense -c food -a 1200 -desc "Pizza slice"` |
| List all | `pipenv run list-expenses` |
| List by category | `pipenv run list-expenses -c transport` |
| List date range  | `pipenv run list-expenses -f 2025-07-01 -t 2025-07-31` |
| Summary (all time) | `pipenv run summary` |
| Summary July 2025, top‑3 | `pipenv run summary -m 2025-07 -n 3` |

**Scripts defined in *Pipfile***

```toml
[scripts]
tracker        = "python tracker.py"
add-expense    = "python tracker.py add"
list-expenses  = "python tracker.py list"
summary        = "python tracker.py summary"
test           = "pytest -q"
```

---

## 🧪 Running Tests

The test suite spins up an **in‑memory SQLite** database, so your real data is safe.

```bash
pipenv run test
# or
pipenv run pytest
```

---

## 🛠️ Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: db` when running tests | Ensure you run tests from project root, or use `pipenv run pytest`. |
| CLI error “Date must be in YYYY‑MM‑DD format” | Enter date like `2025-07-20` (or omit `-d` to default to today). |
| “database is locked” (rare on Windows) | Close other shells using `expenses.db`; SQLite allows one writer at a time. |

---

## 📹 Demo Video

A 3‑minute walkthrough (setup → interactive mode → command mode) is available in the `docs/` folder and on Google Drive:
`expense-tracker-demo-anthony_ngigi.mp4`

---

## 📝 License

MIT — see `LICENSE`.