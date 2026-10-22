# Personal Finance Tracker

A web-based application built with Django to help users manage personal expenses and keep track of their financial activities.

## Features

- **User Authentication:** Sign up and log in to access the application.
- **Expense Management:** Add, view, and manage expense records.
- **Dashboard:** View financial information through a dashboard.
- **Expense Records:** Review and manage saved expenses.
- **User Profile:** Access and manage user profile information.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Project Structure

```text
Personal Finance Tracker/
├── accounts/
├── expenses/
├── finance_tracker/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ummehoney0172-tech/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Future Improvements

- Income tracking and monthly summaries
- Expense categories and filtering
- Visual charts and financial reports
- Improved user interface and user experience

## Author

**Umme Honey Khan Oishi**

GitHub: [ummehoney0172-tech](https://github.com/ummehoney0172-tech)

## License

This project is currently available for educational and portfolio purposes.
