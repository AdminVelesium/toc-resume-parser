#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def convert_json_string_to_dict(json_string: str) -> dict:
    """
    Converts a JSON string (which might be wrapped in extra quotes and have escaped inner quotes)
    into a Python dictionary.

    Args:
        json_string (str): The string representation of a JSON object.

    Returns:
        dict: The Python dictionary equivalent of the JSON string.

    Raises:
        json.JSONDecodeError: If the input string is not a valid JSON format
                              after initial processing.
    """
    try:
        # Step 1: Remove the outermost quotes if they exist.
        # This handles cases where the entire JSON is wrapped like '"json_content"'
        if json_string.startswith('"') and json_string.endswith('"'):
            # Slice the string to remove the first and last characters
            json_string_processed = json_string[1:-1]
        else:
            json_string_processed = json_string

        # Step 2: Unescape any internal double quotes.
        # This converts '\"' back to '"' within the string.
        # This is crucial for json.loads() to correctly parse the JSON structure.
        final_json_string = json_string_processed.replace('\\"', '"')

        # Step 3: Parse the cleaned JSON string into a dictionary.
        data_dict = json.loads(final_json_string)
        return data_dict

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Print a snippet of the string being processed at the time of error
        print(f"Problematic string (or part of it) during json.loads(): {final_json_string[:200]}...")
        raise # Re-raise the exception after printing details for debugging
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise








def fields_to_be_displayed(resume_data):
    # Assuming 'resume_data' is the dictionary you provided
    # (The full dictionary is assumed to be available as 'resume_data' in the environment)

    # --- Personal Details ---
    first_name = resume_data['data']['name'].get('first', '')
    last_name = resume_data['data']['name'].get('last', '')
    email = resume_data['data']['emails'][0] if resume_data['data']['emails'] else ''
    mobile = resume_data['data']['phoneNumbers'][0] if resume_data['data']['phoneNumbers'] else ''
    location = resume_data['data']['location'].get('formatted', '')
    company = None  # 'company' is not directly available in your provided structure for current employment.
                    # You would typically derive this from 'workExperience' if available.
    nationality = None # 'nationality' is not directly available in your provided structure.
    gender = None      # 'gender' is not directly available in your provided structure.
    profile_photo = resume_data.get('headShot', None) # Note: 'headShot' is at the top level, not inside 'data'.
    resume_file = resume_data['meta'].get('pdf', None) # This is the URL to the PDF resume.
    introduction_video = None # 'introductionVideo' is not directly available in your provided structure.


    print("--- Personal Details ---")
    print(f"firstName: {first_name}")
    print(f"lastName: {last_name}")
    print(f"email: {email}")
    print(f"mobile: {mobile}")
    print(f"location: {location}")
    print(f"company: {company}") # Will be None as not found directly
    print(f"nationality: {nationality}") # Will be None as not found directly
    print(f"gender: {gender}") # Will be None as not found directly
    print(f"profilePhoto: {profile_photo}") # Will be None as not found directly in sample
    print(f"resume: {resume_file}")
    print(f"introductionVideo: {introduction_video}") # Will be None as not found directly

    print("\n" + "-"*30 + "\n")

    # --- Education Details (Iterating through all education entries) ---
    # Your sample has multiple education entries, so we'll extract for each.
    education_list = []
    for edu in resume_data['data']['education']:
        degree = edu['accreditation'].get('education', '')
        # For specialization, we can try to extract from 'education' or 'inputStr' if more specific.
        # In your data, 'education' seems to contain the main degree and specialization.
        specialization = edu['accreditation'].get('inputStr', '') if 'ComputerScience andEngineering' in edu['accreditation'].get('education', '') else ''
        university = edu.get('organization', '')
        start_year = edu['dates'].get('startDate', '').split('-')[0] if edu.get('dates') and edu['dates'].get('startDate') else ''
        end_year = edu['dates'].get('completionDate', '').split('-')[0] if edu.get('dates') and edu['dates'].get('completionDate') else ''
        grades = edu['grade'].get('raw', '') if edu.get('grade') else ''
        institution = edu.get('organization', '') # Same as university in this structure

        education_list.append({
            "degree": degree,
            "specialization": specialization,
            "university": university,
            "startYear": start_year,
            "endYear": end_year,
            "grades": grades,
            "institution": institution
        })

    print("--- Education Details ---")
    for i, edu_detail in enumerate(education_list):
        print(f"Education Entry {i+1}:")
        for key, value in edu_detail.items():
            print(f"  {key}: {value}")
        print("-" * 10)

    print("\n" + "-"*30 + "\n")

    # --- Work Experience Details (Iterating through all work experience entries) ---
    # Your provided sample has an empty 'workExperience' list, so this will be empty.
    # However, the structure is provided based on a typical resume parser output.
    work_experience_list = []
    for exp in resume_data['data']['workExperience']:
        job_title = exp.get('title', '') # Assuming 'title' for jobTitle
        employer = exp.get('organization', '') # Assuming 'organization' for employer
        start_date = exp['dates'].get('startDate', '') if exp.get('dates') else ''
        end_date = exp['dates'].get('completionDate', '') if exp.get('dates') else ''
        designation = exp.get('title', '') # Often same as jobTitle
        employment_type = exp.get('employmentType', '') # Assuming an 'employmentType' field
        work_location = exp['location'].get('formatted', '') if exp.get('location') else ''
        experience_summary = exp.get('description', '') # Assuming a 'description' field for summary
        current_job = exp['dates'].get('isCurrent', False) if exp.get('dates') else False

        work_experience_list.append({
            "jobTitle": job_title,
            "employer": employer,
            "startDate": start_date,
            "endDate": end_date,
            "designation": designation,
            "employmentType": employment_type,
            "location": work_location,
            "experienceSummary": experience_summary,
            "currentJob": current_job
        })

    print("--- Work Experience Details ---")
    if work_experience_list:
        for i, exp_detail in enumerate(work_experience_list):
            print(f"Work Experience Entry {i+1}:")
            for key, value in exp_detail.items():
                print(f"  {key}: {value}")
            print("-" * 10)
    else:
        print("No work experience entries found in the provided data.")

    print("\n" + "-"*30 + "\n")

    # # --- Project Details ---
    # # Projects are found within the 'sections' list, specifically under 'sectionType': 'Projects'.
    # project_list = []
    # for section in resume_data['data']['sections']:
    #     if section.get('sectionType') == 'Projects':
    #         # The 'text' field within the 'Projects' section contains the project details.
    #         # This will require more advanced parsing (e.g., regex, NLP) to break down.
    #         # For simplicity, we'll just extract the raw text for now.
    #         # To get structured project details (name, dates, description, skills, URL),
    #         # you'd need to apply more sophisticated text parsing or rely on a dedicated
    #         # project parsing component of the resume parser if it exists.
    #         project_raw_text = section.get('text', '')

    #         # # Dummy extraction for demonstration based on raw text patterns
    #         # # This is highly dependent on the consistency of the raw text format.
    #         # # For 'Speech Buddy'
    #         # if 'Speech Buddy' in project_raw_text:
    #         #     project_list.append({
    #         #         "projectName": "Speech Buddy",
    #         #         "startDate": "November 2024 (implied)", # Extracting actual dates from raw text is complex
    #         #         "endDate": "", # No clear end date in raw text snippet
    #         #         "description": "Developed a React-based web application enabling users to practice spoken English interactively. Utilized Web Speech API for real-time speech recognition and transcription accuracy. Designed a modular frontend with Tailwind CSS for a responsive, visually appealing UI. Implemented robust features like random sentence generation, speech-to-text conversion, and feedback analysis. Conducted extensive testing for transcription accuracy, cross-browser compatibility, and performance.",
    #         #         "keySkills": "React, Web Speech API, Tailwind CSS, Recoil",
    #         #         "projectUrl": "" # Not directly available
    #         #     })
    #         # # For 'CO2 Emission Predictor'
    #         # if 'CO2 Emission Predictor' in project_raw_text:
    #         #     project_list.append({
    #         #         "projectName": "CO2 Emission Predictor",
    #         #         "startDate": "April 2024",
    #         #         "endDate": "",
    #         #         "description": "Developed a model to predict CO2 emissions based on engine size and no. of cylinders. Leveraged various ML models, including Multiple Linear Regression, KNN, Decision Tree, Random Forest, SVM and Passive Aggressive Regressor, to drive accurate predictions. Implemented Neural Networks using Keras, successfully training and fine-tuning models for a dataset of over 1K records. Accurately predicted the CO2 emissions using Random Forest model, attaining R² value of 0.70",
    #         #         "keySkills": "Python, Scikit-learn, TensorFlow, Flask",
    #         #         "projectUrl": ""
    #         #     })
    #         # # For 'Fake News Detection'
    #         # if 'Fake News Detection' in project_raw_text:
    #         #     project_list.append({
    #         #         "projectName": "Fake News Detection",
    #         #         "startDate": "January 2024",
    #         #         "endDate": "March 2024",
    #         #         "description": "Developed a model to classify news as real or fake. Leveraged various ML models, including Naive Bayes, KNN, Logistic Regression, SVM, Random Forest, Passive Aggressive, and Gradient Boosting, to achieve accurate classification on a dataset of over 40,000 records. Accurately classified the news using Random Forest model, attaining accuracy value of 0.997",
    #         #         "keySkills": "Python, Scikit-learn, NLTK, Flask",
    #         #         "projectUrl": ""
    #         #     })
    #         # Note: A real-world parser would have specific fields for each project,
    #         # not just raw text, making extraction much cleaner.

    #         project_list.append(project_raw_text)

    # print("--- Project Details ---")
    # if project_list:
    #     for i, project_detail in enumerate(project_list):
    #         print(f"Project Entry {i+1}:")
    #         for key, value in project_detail.items():
    #             print(f"  {key}: {value}")
    #         print("-" * 10)
    # else:
    #     print("No structured project entries found directly. Manual parsing from 'rawText' would be needed.")





    extracted_info = {
        "personalDetails": {},
        "education": [],
        "workExperience": [],
        "projects": []
    }

    # --- Personal Details ---
    extracted_info["personalDetails"] = {
        "firstName": resume_data['data']['name'].get('first', ''),
        "lastName": resume_data['data']['name'].get('last', ''),
        "email": resume_data['data']['emails'][0] if resume_data['data']['emails'] else '',
        "mobile": resume_data['data']['phoneNumbers'][0] if resume_data['data']['phoneNumbers'] else '',
        "location": resume_data['data']['location'].get('formatted', ''),
        "company": None,  # Not directly available in the provided structure
        "nationality": None, # Not directly available
        "gender": None,      # Not directly available
        "profilePhoto": resume_data.get('headShot', None), # 'headShot' is at the top level, not inside 'data'
        "resume": resume_data['meta'].get('pdf', None), # This is the URL to the PDF resume
        "introductionVideo": None # Not directly available
    }

    # --- Education Details ---
    for edu in resume_data['data']['education']:
        degree = edu['accreditation'].get('education', '')
        specialization = edu['accreditation'].get('inputStr', '') if 'ComputerScience andEngineering' in degree else ''
        university = edu.get('organization', '')
        start_year = edu['dates'].get('startDate', '').split('-')[0] if edu.get('dates') and edu['dates'].get('startDate') else ''
        end_year = edu['dates'].get('completionDate', '').split('-')[0] if edu.get('dates') and edu['dates'].get('completionDate') else ''
        grades = edu['grade'].get('raw', '') if edu.get('grade') else ''
        institution = edu.get('organization', '') # Same as university in this structure

        extracted_info["education"].append({
            "degree": degree,
            "specialization": specialization,
            "university": university,
            "startYear": start_year,
            "endYear": end_year,
            "grades": grades,
            "institution": institution
        })

    # --- Work Experience Details ---
    # Your provided sample has an empty 'workExperience' list, so this will be empty.
    # The structure below assumes a standard work experience object if present.
    for exp in resume_data['data'].get('workExperience', []): # Using .get() with default [] for safety
        job_title = exp.get('title', '')
        employer = exp.get('organization', '')
        start_date = exp['dates'].get('startDate', '') if exp.get('dates') else ''
        end_date = exp['dates'].get('completionDate', '') if exp.get('dates') else ''
        designation = exp.get('title', '')
        employment_type = exp.get('employmentType', '')
        work_location = exp['location'].get('formatted', '') if exp.get('location') else ''
        experience_summary = exp.get('description', '')
        current_job = exp['dates'].get('isCurrent', False) if exp.get('dates') else False

        extracted_info["workExperience"].append({
            "jobTitle": job_title,
            "employer": employer,
            "startDate": start_date,
            "endDate": end_date,
            "designation": designation,
            "employmentType": employment_type,
            "location": work_location,
            "experienceSummary": experience_summary,
            "currentJob": current_job
        })

    # # --- Project Details ---
    # for section in resume_data['data'].get('sections', []):
    #     if section.get('sectionType') == 'Projects':
    #         project_raw_text = section.get('text', '')

    #         extracted_info["projects"].append(project_raw_text)

    #         # These are manually parsed based on the structure of the rawText.
    #         # For a more robust solution, you'd need more sophisticated parsing
    #         # (e.g., regex, NLP) or a parser that provides structured project fields.

    return extracted_info




if __name__=="__main__":
    # Convert the string to a dictionary

    # Your provided JSON string (using raw string r"""...""" to avoid Python's own escape sequence interpretation)
    json_data_string = r"""
    {\"data\":{\"certifications\":[\"Generative AI Introduction and Applications coursera\",\"Generative AI Prompt Engineering Basics coursera\",\"Prompt Engineering for ChatGPT coursera\"],\"dateOfBirth\":null,\"education\":[{\"id\":95426242,\"organization\":\"Kalinga Institute of Industrial Technology\",\"accreditation\":{\"education\":\"B.Tech - ComputerScience andEngineering\",\"educationLevel\":null,\"inputStr\":\"B.Tech - ComputerScience andEngineering\",\"matchStr\":\"\"},\"grade\":{\"raw\":\"(CGPA – 7.4)\",\"value\":\"7.4\",\"metric\":\"CGPA\"},\"location\":{\"formatted\":\"Bhubaneswar, Odisha, India\",\"streetNumber\":null,\"street\":null,\"apartmentNumber\":null,\"city\":\"Bhubaneswar\",\"postalCode\":null,\"state\":\"Odisha\",\"stateCode\":\"OR\",\"country\":\"India\",\"rawInput\":\"Bhubaneswar, Odisha\",\"countryCode\":\"IN\",\"latitude\":20.2960587,\"longitude\":85.8245398,\"poBox\":null},\"dates\":{\"startDate\":\"2021-10-01\",\"completionDate\":\"2025-07-24\",\"isCurrent\":true,\"rawText\":\"October 2021 – Present\"}},{\"id\":95426243,\"organization\":\"Delhi Public School\",\"accreditation\":{\"educationLevel\":null,\"inputStr\":\"\",\"matchStr\":\"\"},\"grade\":null,\"location\":{\"formatted\":\"Panipat, Haryana, India\",\"streetNumber\":null,\"street\":null,\"apartmentNumber\":null,\"city\":\"Panipat\",\"postalCode\":null,\"state\":\"Haryana\",\"stateCode\":\"HR\",\"country\":\"India\",\"rawInput\":\"Panipat\",\"countryCode\":\"IN\",\"latitude\":29.3909464,\"longitude\":76.9635023,\"poBox\":null},\"dates\":{\"startDate\":\"2019-06-01\",\"completionDate\":\"2021-05-01\",\"isCurrent\":false,\"rawText\":\"June 2019 – May 2021\"}},{\"id\":95426244,\"organization\":\"Senior Secondary\",\"accreditation\":{\"educationLevel\":null,\"inputStr\":\"\",\"matchStr\":\"\"},\"grade\":{\"raw\":\"Percentage 87%\",\"value\":\"87%\",\"metric\":\"Percentage\"},\"location\":{\"formatted\":\"Haryana, India\",\"streetNumber\":null,\"street\":null,\"apartmentNumber\":null,\"city\":null,\"postalCode\":null,\"state\":\"Haryana\",\"stateCode\":\"HR\",\"country\":\"India\",\"rawInput\":\"Haryana\",\"countryCode\":\"IN\",\"latitude\":29.0587757,\"longitude\":76.085601,\"poBox\":null},\"dates\":null}],\"emails\":[\"aritrapattanayak901120@gmail.com\",\"priyanshu77288@gmail.com\"],\"location\":{\"formatted\":\"Panipat, Haryana, India\",\"streetNumber\":null,\"street\":null,\"apartmentNumber\":null,\"city\":\"Panipat\",\"postalCode\":null,\"state\":\"Haryana\",\"stateCode\":\"HR\",\"country\":\"India\",\"rawInput\":\"Panipat, Haryana\",\"countryCode\":\"IN\",\"latitude\":29.3909464,\"longitude\":76.9635023,\"poBox\":null},\"name\":{\"raw\":\"ARITRA PATTANAYAK\",\"last\":\"Pattanayak\",\"first\":\"Aritra\",\"title\":\"\",\"middle\":\"\"},\"objective\":\"\",\"phoneNumbers\":[\"+917082049656\"],\"phoneNumberDetails\":[{\"rawText\":\"+917082049656\",\"formattedNumber\":\"+91 70820 49656\",\"countryCode\":\"IN\",\"internationalCountryCode\":91,\"nationalNumber\":\"070820 49656\"}],\"publications\":[],\"referees\":[],\"sections\":[{\"sectionType\":\"PersonalDetails\",\"pageIndex\":0,\"text\":\"ARITRA PATTANAYAK \\nPanipat, Haryana \\nƒ +91 - 7082049656 # aritrapattanayak901120@gmail.com ï linkedin.com / in / Aritra \\n§ github.com / Arnine9112 \",\"bbox\":[48.815113,20.790405,558.5236,68.59973]},{\"sectionType\":\"Education\",\"pageIndex\":0,\"text\":\"Education \\n\\nKalinga Institute of Industrial Technology October 2021 – Present B.Tech - ComputerScience andEngineering (CGPA – 7.4) Bhubaneswar, Odisha \\n\\nDelhi Public School, Panipat Refinery June 2019 – May 2021 Senior Secondary Panipat, Haryana Percentage – 87% \",\"bbox\":[29.225443,77.453125,581.91254,173.91437]},{\"sectionType\":\"Training/Certifications\",\"pageIndex\":0,\"text\":\"Relevant Coursework \\n• \",\"bbox\":[29.254286,189.93927,153.73184,215.21954]},{\"sectionType\":\"Education\",\"pageIndex\":0,\"text\":\"Data Structures and Algorithms(DSA) \\n• Operating Systems \\n• Cloud Computing \\n• Software Engineering \\n• DBMS \\n• OOPs \\n• Machine Learning \\n• Big Data \\n• Artificial Intelligence \\n• Data Analytics \\n• Computer Networks \",\"bbox\":[47.354916,209.5257,561.25464,240.61938]},{\"sectionType\":\"Projects\",\"pageIndex\":0,\"text\":\"Projects \\nSpeech Buddy | React, Web Speech API, Tailwind CSS, Recoil November 2024 \\n• Developed a React - based web application enabling users to practice spoken English interactively. \\n• Utilized Web Speech API for real - time speech recognition and transcription accuracy. \\n• Designed a modular frontend with Tailwind CSS for a responsive, visually appealing UI. \\n• Implemented robust features like random sentence generation, speech - to - text conversion, and feedback analysis. \\n• Conducted extensive testing for transcription accuracy, cross - browser compatibility, and performance. \\n\\nCO2 Emission Predictor | Python, Scikit - learn, TensorFlow, Flask April 2024 \\n• Developed a model to predict CO2 emissions based on engine size and no. of cylinders. \\n• Leveraged various ML models, including Multiple Linear Regression, KNN, Decision Tree, Random Forest, SVM and Passive Aggressive Regressor, to drive accurate predictions. \\n• Implemented Neural Networks using Keras, successfully training and fine - tuning models for a dataset of over 1K records. \\n• Accurately predicted the CO2 emissions using Random Forest model, attaining R² value of 0.70 \\n\\nFake News Detection | Python, Scikit - learn, NLTK, Flask January 2024 – March 2024 \\n• Developed a model to classify news as real or fake. \\n• Leveraged various ML models, including Naive Bayes, KNN, Logistic Regression, SVM, Random Forest, Passive Aggressive, and Gradient Boosting, to achieve accurate classification on a dataset of over 40,000 records. \\n• Accurately classified the news using Random Forest model, attaining accuracy value of 0.997 \",\"bbox\":[29.1885,250.69202,582.677,546.4173]},{\"sectionType\":\"Skills/Interests/Languages\",\"pageIndex\":0,\"text\":\"Technical Skills \\n\\nLanguages: C, C++, Java, Python, HTML / CSS, SQL Technologies / Frameworks: Scikit - learn, NumPy, Pandas, TensorFlow, Matplotlib, Streamlit Developer Tools: VS Code, Git, GitHub, Jupyter Notebook, Google Collab, Kaggle, PyCharm \",\"bbox\":[29.290121,556.9523,462.29776,609.12634]},{\"sectionType\":\"Training/Certifications\",\"pageIndex\":0,\"text\":\"Certifications \\n• Problem Solving (Basic) - HackerRank \\n• Problem Solving (Intermediate) - HackerRank \\n• Generative AI: Introduction and Applications - coursera \\n• Generative AI: Prompt Engineering Basics - coursera \\n• Prompt Engineering for ChatGPT - coursera \",\"bbox\":[29.541225,621.1324,301.25156,725.1353]}],\"skills\":[{\"id\":1109779930,\"emsiId\":\"KS125LS6N7WP4S6SFTCK\",\"name\":\"Python (Programming Language)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779931,\"emsiId\":\"KS121F45VPV8C9W3QFYH\",\"name\":\"Cascading Style Sheets (CSS)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779932,\"emsiId\":\"ES36640EBD9133DC4BB2\",\"name\":\"Prompt Engineering\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Training/Certifications\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779933,\"emsiId\":\"ESD5C3FF77F38D04C794\",\"name\":\"Gradient Boosting\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779934,\"emsiId\":\"KS441WZ6SHN10VW7Q4MZ\",\"name\":\"Speech Recognition\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779935,\"emsiId\":\"KS125Z169HQJ1KQT60RW\",\"name\":\"Logistic Regression\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779936,\"emsiId\":\"KS125F678LV2KB3Z5XW0\",\"name\":\"Problem Solving\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"common_skill\",\"sources\":[{\"section\":\"Training/Certifications\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779937,\"emsiId\":\"KSGWPO6DSN70GRY20JFT\",\"name\":\"Pandas (Python Package)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779938,\"emsiId\":\"KS1274P66LZKSR1F2YCT\",\"name\":\"NumPy (Python Package)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779939,\"emsiId\":\"KS440W865GC4VRBW6LJP\",\"name\":\"SQL (Programming Language)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779941,\"emsiId\":\"KS1271Z6ZP3RPMKFFCK7\",\"name\":\"NLTK (NLP Analysis)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779942,\"emsiId\":\"KS1208P6ZMZ4N872Y7X5\",\"name\":\"Application Programming Interface (API)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779944,\"emsiId\":\"KSIF64ADSNL8EWGKPF0O\",\"name\":\"Dataset\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779949,\"emsiId\":\"KS1200364C9C1LK3V5Q1\",\"name\":\"C (Programming Language)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"PersonalDetails\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Training/Certifications\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779950,\"emsiId\":\"KS124CH623PFBJS8T5KM\",\"name\":\"Github\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"PersonalDetails\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779952,\"emsiId\":\"ES5AE3072EC6678972A3\",\"name\":\"Multiple Linear Regression\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779953,\"emsiId\":\"KSFHF2FU8HN39495VYLU\",\"name\":\"Keras (Neural Network Library)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779954,\"emsiId\":\"KS1217278SZ35V5NJM37\",\"name\":\"Browser Compatibility\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779956,\"emsiId\":\"ESA91D8112EB9ECA3570\",\"name\":\"Git (Version Control System)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"PersonalDetails\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779957,\"emsiId\":\"KSFDBQT68SA9R0I0SAVH\",\"name\":\"Jupyter\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779959,\"emsiId\":\"KS120076FGP5WGWYMP0F\",\"name\":\"Java (Programming Language)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779960,\"emsiId\":\"KS1200578T5QCYT0Z98G\",\"name\":\"HyperText Markup Language (HTML)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779940,\"emsiId\":\"ES271C4EB47A4BD5AD68\",\"name\":\"VS Code\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779943,\"emsiId\":\"KS1233365B2V7G3HN4HW\",\"name\":\"Transcription (Genetics)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779945,\"emsiId\":\"ES46B2FBE34B5D3E45D5\",\"name\":\"Flask (Web Framework)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779946,\"emsiId\":\"KSXP0ABTAF9E0XOQ1MTF\",\"name\":\"Jupyter Notebook\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779947,\"emsiId\":\"KSORG41MPDZUG1W4O6M6\",\"name\":\"Boosting\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779948,\"emsiId\":\"KS2GHRCYA6TRT29F1HOO\",\"name\":\"TensorFlow\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null},{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779951,\"emsiId\":\"KS126796RG0M9JRLKDQY\",\"name\":\"Matplotlib (Python Package)\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779955,\"emsiId\":\"KS128836KV2F3BRZK1ZG\",\"name\":\"PyCharm\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Skills/Interests/Languages\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779961,\"emsiId\":\"KS125VJ636ZVWXWBJH1C\",\"name\":\"Linear Regression\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Projects\",\"position\":null,\"workExperienceId\":null}]},{\"id\":1109779962,\"emsiId\":\"ES2BB25DB544B26CD7AA\",\"name\":\"ChatGPT\",\"lastUsed\":null,\"numberOfMonths\":null,\"type\":\"specialized_skill\",\"sources\":[{\"section\":\"Training/Certifications\",\"position\":null,\"workExperienceId\":null}]}],\"languages\":[\"English\"],\"summary\":\"\",\"websites\":[\"https://www.linkedin.com/in/aritra-pattanayak-7bbb16262/\",\"https://github.com/arnine9112\"],\"linkedin\":\"https://www.linkedin.com/in/aritra-pattanayak-7bbb16262/\",\"totalYearsExperience\":0,\"profession\":null,\"workExperience\":[],\"headShot\":null,\"isResumeProbability\":null,\"rawText\":\"ARITRA PATTANAYAK \\nPanipat, Haryana \\nƒ +91 - 7082049656 # aritrapattanayak901120@gmail.com ï linkedin.com / in / Aritra \\n§ github.com / Arnine9112 \\nEducation \\n\\nKalinga Institute of Industrial Technology October 2021 – Present B.Tech - ComputerScience andEngineering (CGPA – 7.4) Bhubaneswar, Odisha \\n\\nDelhi Public School, Panipat Refinery June 2019 – May 2021 Senior Secondary Panipat, Haryana Percentage – 87% \\nRelevant Coursework \\n• \\nData Structures and Algorithms(DSA) \\n• Operating Systems \\n• Cloud Computing \\n• Software Engineering \\n• DBMS \\n• OOPs \\n• Machine Learning \\n• Big Data \\n• Artificial Intelligence \\n• Data Analytics \\n• Computer Networks \\nProjects \\nSpeech Buddy | React, Web Speech API, Tailwind CSS, Recoil November 2024 \\n• Developed a React - based web application enabling users to practice spoken English interactively. \\n• Utilized Web Speech API for real - time speech recognition and transcription accuracy. \\n• Designed a modular frontend with Tailwind CSS for a responsive, visually appealing UI. \\n• Implemented robust features like random sentence generation, speech - to - text conversion, and feedback analysis. \\n• Conducted extensive testing for transcription accuracy, cross - browser compatibility, and performance. \\n\\nCO2 Emission Predictor | Python, Scikit - learn, TensorFlow, Flask April 2024 \\n• Developed a model to predict CO2 emissions based on engine size and no. of cylinders. \\n• Leveraged various ML models, including Multiple Linear Regression, KNN, Decision Tree, Random Forest, SVM and Passive Aggressive Regressor, to drive accurate predictions. \\n• Implemented Neural Networks using Keras, successfully training and fine - tuning models for a dataset of over 1K records. \\n• Accurately predicted the CO2 emissions using Random Forest model, attaining R² value of 0.70 \\n\\nFake News Detection | Python, Scikit - learn, NLTK, Flask January 2024 – March 2024 \\n• Developed a model to classify news as real or fake. \\n• Leveraged various ML models, including Naive Bayes, KNN, Logistic Regression, SVM, Random Forest, Passive Aggressive, and Gradient Boosting, to achieve accurate classification on a dataset of over 40,000 records. \\n• Accurately classified the news using Random Forest model, attaining accuracy value of 0.997 \\nTechnical Skills \\n\\nLanguages: C, C++, Java, Python, HTML / CSS, SQL Technologies / Frameworks: Scikit - learn, NumPy, Pandas, TensorFlow, Matplotlib, Streamlit Developer Tools: VS Code, Git, GitHub, Jupyter Notebook, Google Collab, Kaggle, PyCharm \\nCertifications \\n• Problem Solving (Basic) - HackerRank \\n• Problem Solving (Intermediate) - HackerRank \\n• Generative AI: Introduction and Applications - coursera \\n• Generative AI: Prompt Engineering Basics - coursera \\n• Prompt Engineering for ChatGPT - coursera \",\"redactedText\":\"****** ********** ******** ******* ƒ *** * ********** # ******************************** ï ************ / in / ****** § ********** / Arnine9112\\nEducation Kalinga Institute of Industrial Technology ******* **** – Present B.Tech - ComputerScience andEngineering (CGPA – 7.4) Bhubaneswar, Odisha Delhi Public School, Panipat Refinery **** **** – *** **** Senior Secondary Panipat, Haryana Percentage – 87%\\nRelevant Coursework •\\nData Structures and Algorithms(DSA) • Operating Systems • Cloud Computing • Software Engineering • DBMS • OOPs • Machine Learning • Big Data • Artificial Intelligence • Data Analytics • Computer Networks\\nProjects Speech Buddy | React, Web Speech API, Tailwind CSS, Recoil ******** **** • Developed a React - based web application enabling users to practice spoken English interactively. • Utilized Web Speech API for real - time speech recognition and transcription accuracy. • Designed a modular frontend with Tailwind CSS for a responsive, visually appealing UI. • Implemented robust features like random sentence generation, speech - to - text conversion, and feedback analysis. • Conducted extensive testing for transcription accuracy, cross - browser compatibility, and performance. CO2 Emission Predictor | Python, Scikit - learn, TensorFlow, Flask ***** **** • Developed a model to predict CO2 emissions based on engine size and no. of cylinders. • Leveraged various ML models, including Multiple Linear Regression, KNN, Decision Tree, Random Forest, SVM and Passive Aggressive Regressor, to drive accurate predictions. • Implemented Neural Networks using Keras, successfully training and fine - tuning models for a dataset of over 1K records. • Accurately predicted the CO2 emissions using Random Forest model, attaining R² value of 0.70 Fake News Detection | Python, Scikit - learn, NLTK, Flask ******* **** – ***** **** • Developed a model to classify news as real or fake. • Leveraged various ML models, including Naive Bayes, KNN, Logistic Regression, SVM, Random Forest, Passive Aggressive, and Gradient Boosting, to achieve accurate classification on a dataset of over 40,000 records. • Accurately classified the news using Random Forest model, attaining accuracy value of *****\\nTechnical Skills Languages: C, C++, Java, Python, HTML / CSS, SQL Technologies / Frameworks: Scikit - learn, NumPy, Pandas, TensorFlow, Matplotlib, Streamlit Developer Tools: VS Code, Git, GitHub, Jupyter Notebook, Google Collab, Kaggle, PyCharm\\nCertifications • Problem Solving (Basic) - HackerRank • Problem Solving (Intermediate) - HackerRank • Generative AI: Introduction and Applications - coursera • Generative AI: Prompt Engineering Basics - coursera • Prompt Engineering for ChatGPT - coursera\"},\"meta\":{\"identifier\":\"TAOVQKPI\",\"customIdentifier\":null,\"ready\":true,\"failed\":false,\"readyDt\":\"2025-07-24T16:08:09.406475Z\",\"fileName\":\"aritra_resume.pdf\",\"expiryTime\":null,\"language\":\"en\",\"pdf\":\"https://affinda-api-data-prod-ap1.s3.amazonaws.com/media/documents/aritra_resume_S4O8RYT.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAU4IX6YWNM3WTEPIA%2F20250724%2Fap-southeast-2%2Fs3%2Faws4_request&X-Amz-Date=20250724T160809Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAgaDmFwLXNvdXRoZWFzdC0yIkYwRAIgHsspHuhYQ1w%2FNQv2QOgqyKiBhTfiDit7c81xJhsLLMwCIGuP0PSiXtmhMssCqvzZje6ASnzlcrZJuB%2FMjTO1LMVFKokFCDEQAxoMMzM1NTk0NTcxMTYyIgyezWPtQGoem26M8Qsq5gR9GPHwVAKTSAp94CkXB%2FKRZ60h2EQOO91UHr%2FD3i86y0oVwhdL3aOlqW8viXIGnTKv79ru%2B5134XoY6e41Kpem0WEDLCoE4f%2FMc2ez5%2Brl%2BG6QhgIIna8I4%2BGcG4AYxusu4EnR05DLSj0J%2Bzfx1rt0goA9iUk%2BWHkqmPLE6IZN1Imjqi56RMnbJBZd3upKjxdc4sJbC1GezHkaiudmjDn4Xv8W9caM%2BAtaN9BxVBJoAYYQeyq5iQrREqGg093bH17pXPIkjkH23zP9qoglxHw9Z2bWkbDNJWjhR2wj%2FdZpRxuEDCrTZ9SrbiQE12SK%2BZ3c2Tuo254QUfeZHxqBjU1SnVWBTeh%2BjAUFFbPg5gCIkIsfor%2BGHHJGVsqruWQWqF5GGXkWTJPPGhNJ6rrHJ%2BAY44XTfCyKfDQoaGEaxrI65RFPC%2FH4kDQkuWajXM2V7XxIWX9tRzSa4qDihMbS0RIrZAa9Tz%2BxrW9wIj3LyGw4Hy9jmjYdAWNAx5jeFMKZiFRHJuB%2BuRPoux9LZreC1dSnUw4HkNAuMcbOl6sJIdR8Mnh1Nb6xNhmMWINCtbz5dB48GLQICdR6Fxce%2BzNjp1kRuOjkIUIMejb8RxERZ2APzEXlgSvbUdnXDXcIVD7d%2FsfhussQVhe9IL6PNRECcEOY5MyyLkIwiOr1gBad%2Fdiux1BHppXJjzMfs%2BujYD5OGSrWhWm1pH0fxDvVlQC0Up2Xh26ZHYMvcy0iaNSiofxYE1I2euirb71xur%2BNHvcZdQ8oU8EGdEt%2BCx%2BAj07NcEq6d8Puy38BVK78RXhEiu0WqTWe8%2FgD9TC2sInEBjqbAQuzevSbOJUcs5Jy8YoL3WidlDvT%2BZVY6XnI%2BAammhsY4IjMqMbjwuazCnR%2Fn1AhpUWrES4dDFenrIzSYXLVCxzDMGUroesq5tajy4B1HKDi9b7p4mzfGKK5gpn2GM9HkkuzXM4yg3pIyZrGcUy18ZqYdwToVbLHGd846sksYvhUvanHccWdaKE%2BF8fCiPWT1rmjgKiauIztJ0Oe&X-Amz-Signature=6b343b86764f22668d6fe8427398c248dc5cf15638daf8f932bd60af69dea66f\",\"regionBias\":null,\"isOcrd\":false},\"error\":{\"errorCode\":null,\"errorDetail\":null}}
    """
    try:
        resume_data = convert_json_string_to_dict(json_data_string)

        # You can now work with the dictionary
        print(f"Successfully converted to dictionary. Type: {type(resume_data)}")
        # print(json.dumps(result_dict, indent=2)) # Uncomment to print the formatted dictionary
        print(f"First certification: {resume_data['data']['certifications'][0]}")
        print(f"Education (first item organization): {resume_data['data']['education'][0]['organization']}")
        #print(f"Redacted text length: {len(result_dict['redactedText'])}")

        #print(result_dict)
        # Assuming 'resume_data' is the dictionary you provided
        # (The full dictionary is assumed to be available as 'resume_data' in the environment)

        extracted_info = fields_to_be_displayed(resume_data)

        print("Extracted Info \n\n")
        print(extracted_info)


    except Exception as e:
        print(f"Failed to process JSON string: {e}")