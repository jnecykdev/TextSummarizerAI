from flask import Flask, render_template, request, redirect, url_for
import PyPDF2  # Import PyPDF2 for PDF reading
import os # Import os for path manipulation and directory creation
from datetime import datetime # Import datetime for unique filenames

# Assuming main.py is in the same directory and contains the TextSummarizer class
from main import TextSummarizer

app = Flask(__name__)
summarizer = TextSummarizer()

# Configuration for the output folder
# This folder will be created inside your project directory
OUTPUT_FOLDER = 'medias'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER) # Create the folder if it doesn't exist

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(url_for('index', error="No file part in the request."))
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(url_for('index', error="No selected file."))

        text_to_summarize = ""
        # Check if the uploaded file is a PDF
        if file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file)
            if extracted_text is None:
                return redirect(url_for('index', error="Failed to extract text from PDF. Is it a valid PDF?"))
            text_to_summarize = extracted_text
        else: # Assume it's a text file
            try:
                text_to_summarize = file.read().decode("utf-8")
            except Exception as e:
                return redirect(url_for('index', error=f"Error reading text file: {e}"))

        if not text_to_summarize.strip():
            return redirect(url_for('index', error="The uploaded file is empty or contains no readable text."))

        # Call the summarizer from main.py
        raw_summary = summarizer.summarize(text_to_summarize)
        
        summary = raw_summary # The summarize method in main.py now returns a clean string

        # --- New functionality: Save summary to a file ---
        try:
            # Create a unique filename using timestamp and original filename (if available)
            original_filename_base = os.path.splitext(file.filename)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"summary_{original_filename_base}_{timestamp}.txt"
            output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)

            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Summary successfully saved to: {output_filepath}")
            # Optionally, you could pass a success message to the template
            # return render_template("index.html", summary=summary, file_saved_message=f"Summary saved to {output_filename}")
        except Exception as e:
            print(f"Error saving summary to file: {e}")
            # Redirect with an error if saving fails, but still show summary in browser
            return redirect(url_for('index', error=f"Summary generated, but failed to save to file: {e}"))
        # --- End of new functionality ---

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
