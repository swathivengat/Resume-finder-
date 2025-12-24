import requests
import json

BASE_URL = "http://127.0.0.1:5000"

RESUME_FILE_1 = "resume_example_python.pdf"
RESUME_FILE_2 = "resume_example_java.pdf"

JOB_DESCRIPTION_HR = {
    "description": "We are looking for a highly skilled Python developer with experience in machine learning frameworks like scikit-learn and deep understanding of data structures."
}

def upload_resume(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            response = requests.post(f"{BASE_URL}/upload_resume", files=files)

        print(f"\n--- Upload Result for {file_path} ---")
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        return response
    except FileNotFoundError:
        print(f"\n[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"\n[ERROR] An error occurred during upload: {e}")

def match_resumes(job_description_data):
    try:
        print("\n--- Sending Job Description for Matching ---")
        response = requests.post(
            f"{BASE_URL}/match_resume",
            json=job_description_data
        )

        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        return response
    except Exception as e:
        print(f"\n[ERROR] An error occurred during matching: {e}")

if __name__ == "__main__":
    print("Starting backend API tests...")

    upload_resume(RESUME_FILE_1)
    upload_resume(RESUME_FILE_2)
    match_resumes(JOB_DESCRIPTION_HR)

    print("\nTests complete. Check the output above and the server terminal for printed logs.")
