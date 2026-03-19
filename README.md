# HopeLog

HopeLog is a Django-based web application designed to help users track their daily habits and learning progress.

## 🌟 Key Features
* **User Authentication:** Secure registration and login system via the `accounts` app.
* **Dashboard:** A central hub to view an overview of your progress.
* **Habit Tracker:** Log and monitor your daily routines and habits.
* **Learning Tracker:** Keep a record of the subjects or skills you are actively learning.

## 🛠️ Tech Stack
* **Framework:** Django (Python)
* **Databases:** SQLite for local development, configured for PostgreSQL in production.
* **Deployment Setup:** Configured with `whitenoise` for static files, `gunicorn` for the web server, and `dj-database-url`.

## 💻 How to Run Locally

1. **Activate the Virtual Environment**
   Open your terminal in the project directory and run:
   ```cmd
   .\.venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**
   This prepares your local SQLite database:
   ```cmd
   python manage.py migrate
   ```

4. **Start the Server**
   ```cmd
   python manage.py runserver
   ```
   *Your app will now be live locally at `http://localhost:8000`*

## 🚀 Production Deployment
This application is fully prepared to be hosted on platforms like **Render**. 
It uses the included `build.sh` script to automatically run migrations and setup static files during the deployment process.
