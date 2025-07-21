# TextSummarizerAI

This is a simple web application built with Flask that allows you to upload text or PDF files and get a concise summary using the spaCy library.

# Project Structure
project/
│


├── main.py             # Contains the TextSummarizer class with spaCy logic


├── app.py              # The main Flask application


├── templates/


│   └── index.html      # Frontend HTML for the web interface


├── static/


│   └── styles.css      # CSS for styling the web interface


└── summaries/          # Folder where generated summaries will be saved (created automatically)

**Setup and Running Instructions**

Follow these steps to get the application up and running on your local machine.

Prerequisites
Python 3.x: Ensure you have Python 3 installed. You can download it from python.org.

pip: Python's package installer. It usually comes with Python 3.

venv: Python's module for creating virtual environments. It also comes with Python 3.

**Step-by-Step Guide**
**Navigate to the Project Directory**

Open your terminal or command prompt and navigate to the project/ directory where your app.py, main.py, templates/, and static/ folders are located.

cd path/to/your/project

(Replace path/to/your/project with the actual path to your project folder.)

**Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies. This isolates your project's packages from your system-wide Python installation.

python3 -m venv venv

**Activate the Virtual Environment**

On macOS/Linux:

source venv/bin/activate

On Windows (Command Prompt):

venv\Scripts\activate.bat

On Windows (PowerShell):

.\venv\Scripts\Activate.ps1

You should see (venv) at the beginning of your terminal prompt, indicating that the virtual environment is active.

**Install Required Python Packages**

First, let's create a requirements.txt file with the necessary packages. In your project/ directory, create a new file named requirements.txt and add the following content:

Flask
PyPDF2
spacy

Now, install these packages using pip:

pip install -r requirements.txt

**Download the spaCy Language Model**
Since the application uses spaCy, you need to download the English language model.

python3 -m spacy download en_core_web_sm

**Run the Flask Application**
With the virtual environment active and all dependencies installed, you can now run the Flask application:

python3 app.py

The Flask development server will start, and you should see output similar to this:

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX

**Access the Application in Your Browser**
Open your web browser and navigate to the address provided in the terminal, usually:

http://127.0.0.1:5000/

You can now upload text or PDF files to get their summaries. Summaries will also be saved in the summaries/ folder within your project directory.
