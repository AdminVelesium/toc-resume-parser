import requests
import os
import json

# Define the API endpoint URL
API_URL = "http://localhost:8000/parse_uploaded_resume"

# Define the path to your sample resume file
# Make sure this path is correct on your machine
SAMPLE_RESUME_PATH = "sumanth_resume.pdf" # Or full path like "/Users/youruser/Documents/sample_resume.pdf"

if not os.path.exists(SAMPLE_RESUME_PATH):
    print(f"Error: Sample resume file not found at '{SAMPLE_RESUME_PATH}'. Please check the path.")
else:
    try:
        # Open the file in binary read mode
        with open(SAMPLE_RESUME_PATH, 'rb') as f:
            # Prepare the 'files' dictionary for requests.post
            # The key 'file' must match what your Flask app expects (request.files['file'])
            # The tuple format is (filename, file_object, content_type)
            files = {
                'file': (os.path.basename(SAMPLE_RESUME_PATH), f, 'application/pdf')
            }

            print(f"Sending '{SAMPLE_RESUME_PATH}' to {API_URL}...")
            response = requests.post(API_URL, files=files)

        # Check if the request was successful
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

        # Print the JSON response from the Flask app
        print("API Response:")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")