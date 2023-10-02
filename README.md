# BankApp-flask
Python, Flask, HTML.

# Flask App README

This repository contains a Flask web application that functions as a basic banking app.

## Prerequisites

Before running the Flask app, ensure you have the following prerequisites installed:

- Python 3.7 or higher
- Flask 2.0.1 or higher

## Installation

Follow these steps to set up and run the Flask app:

1. Clone the repository:
   `````shell
   git clone https://github.com/1deyce/BankApp-flask.git 
   ```

2. Navigate to the project directory:
   ````shell
   cd BankApp-flask
   ```

3. Create and activate a virtual environment (optional, but recommended):
   ````shell
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ````shell
   pip install -r requirements.txt
   ```

5. Set the Flask app environment variable:
   - For Linux/Mac:
     ````shell
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```

   - For Windows (PowerShell):
     ````shell
     $env:FLASK_APP = "app.py"
     $env:FLASK_ENV = "development"
     ```

6. Run the Flask app:
   ````shell
   flask run
   ```

7. Open a web browser and go to `http://localhost:5000` to access the Flask app.
