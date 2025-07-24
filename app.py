import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from processors import convert_json_string_to_dict, fields_to_be_displayed

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Affinda API Configuration ---
AFFINDA_API_KEY = os.getenv("AFFINDA_API_KEY")
AFFINDA_URL = "https://api.affinda.com/v2/resumes" # Affinda's resume parsing endpoint
HEADERS = {
    "Authorization": f"Bearer {AFFINDA_API_KEY}"
}

# Basic validation for API key
if not AFFINDA_API_KEY:
    app.logger.error("AFFINDA_API_KEY is not set in environment variables. Affinda parsing will not work.")
    # In a production app, you might want to raise an error or return a 500 here.

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Checks if the uploaded file's extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def test():

    return "Congratulations ! The app is working !!"
    

@app.route("/parse_uploaded_resume", methods=["POST"])
def parse_uploaded_resume():
    """
    API endpoint to receive an uploaded resume file and send it to Affinda for parsing.
    Expects a file under the 'file' key in multipart/form-data.
    """
    # Check if the 'file' part is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request. Please upload a file with key 'file'."}), 400

    file = request.files['file']

    # Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    try:
        # Affinda API expects the file to be sent in binary mode.
        # The `file` object from Flask's request.files is already a file-like object.
        # We can directly pass its `stream` attribute or the file itself.
        # It's good practice to provide a filename and content type.
        files_to_send = {
            "file": (file.filename, file.stream, file.content_type)
        }
        
        app.logger.info(f"Received file: {file.filename} ({file.content_type}). Sending to Affinda API.")

        response = requests.post(AFFINDA_URL, headers=HEADERS, files=files_to_send)

        if response.status_code == 201:
            app.logger.info("Affinda API successfully parsed resume.")
            output = jsonify(response.json())

            resume_data = convert_json_string_to_dict(response.text)
            # print(resume_data)
            extracted_info = fields_to_be_displayed(resume_data)
            #return output
            return json.dumps(extracted_info, indent=None)

        else:
            app.logger.error(f"Affinda API failed: Status {response.status_code}, Message: {response.text}")
            # return jsonify({
            #     "error": "Affinda API failed to parse resume.",
            #     "status_code": response.status_code,
            #     "message": response.text
            # }), 500
            resume_data = convert_json_string_to_dict(response.text)
            print(resume_data)
            extracted_info = fields_to_be_displayed(resume_data)
            # return extracted_info
            return json.dumps(extracted_info, indent=None)

    except requests.exceptions.RequestException as req_e:
        app.logger.error(f"Network or request error when calling Affinda API: {req_e}", exc_info=True)
        return jsonify({"error": f"Network or API communication error: {str(req_e)}"}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred during file processing: {e}", exc_info=True)
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    # Flask app will run on host 0.0.0.0 to be accessible from outside the container (e.g., Render)
    # and use the PORT environment variable if set, otherwise default to 5000.
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", 5000))

