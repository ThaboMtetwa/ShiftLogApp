# ShiftLogApp

Shift Log App

Shift Log App is a simple web-based application built with Flask and SQLAlchemy to manage worker shifts. The application allows you to add new workers, log shifts, view shift logs, and export data to CSV files.

*This project is not complete and is an ongoing work in process.*

Features

Worker Management:Add new workers with details like employee number, first name, last name, and pay tier.

Shift Logging:Log shift details (start time, end time, hours worked, and pay earned) for each worker.

Data Export:Export worker and shift data to CSV files for easy reporting and backup.

Dashboard:A clean and intuitive dashboard to view shift logs and perform actions.

Installation

Clone the Repository:

git clone https://your.repo.url/shift-log-app.git
cd shift-log-app

Set Up a Virtual Environment:

python -m venv .venv
source .venv/bin/activate   

On Windows use: .venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Configure Environment Variables (Optional):

You can set the following environment variables if needed:

SECRET_KEY: Flask secret key.

DATABASE_URL: Database connection string (defaults to sqlite:///shift_management.db).

Running the Application

Run the Flask Development Server:

flask run

Access the App:Open your browser and go to http://127.0.0.1:5000 to access the Shift Management Dashboard.

Usage

Dashboard:The main dashboard allows you to view all workers, select a worker to view shift logs, and access actions such as adding a new worker or exporting data.

Add Worker:Use the "Add a New Worker" button to add worker details.

Log Shift:Select a worker from the dropdown, then use the "Log Shift" button to log a new shift.

Export Data:Export worker or shift data to CSV using the corresponding buttons.

Configuration

Database:The application uses SQLite as the database. The connection is configured in app/config.py.

Application Settings:Other settings such as SQLALCHEMY_TRACK_MODIFICATIONS and SECRET_KEY are also defined in app/config.py.

Development Notes

Database Schema:Tables are created automatically if the app is running in the development environment (controlled by the ENV variable).

Session Management:A teardown function is set up in app/__init__.py to remove the SQLAlchemy session after each request.
