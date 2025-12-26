import os
import re
import nltk
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

SKILL_SET = {
    "python", "java", "c++", "c",
    "machine learning", "deep learning",
    "data science", "data analysis",
    "nlp", "artificial intelligence",
    "sql", "mysql", "postgresql",
    "tensorflow", "pytorch", "scikit-learn",
    "flask", "fastapi", "django",
    "html", "css", "javascript",
    "react", "node", "git", "docker", "linux"
}

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RESUME_DATA = {}

lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        return text
    except Exception:
        return None

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    cleaned_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens if word not in STOPWORDS
    ]
    return " ".join(cleaned_tokens)

def extract_skills(text):
    found_skills = set()
    for skill in SKILL_SET:
        if skill in text:
            found_skills.add(skill)
    return sorted(found_skills)

def get_similarity_score(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf)[0][1]
    return round(score * 100, 2)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/hr')
def hr():
    return render_template('hr.html')

@app.route('/upload_resume', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text_from_pdf(file_path)
    if not resume_text:
        os.remove(file_path)
        return jsonify({'error': 'Could not read PDF'}), 500

    cleaned_resume_text = clean_text(resume_text)
    resume_skills = extract_skills(cleaned_resume_text)

    RESUME_DATA[filename] = {
        'cleaned_text': cleaned_resume_text,
        'original_name': filename,
        'skills': resume_skills
    }

    os.remove(file_path)
    return jsonify({'message': 'Resume processed successfully!', 'filename': filename}), 200

@app.route('/match_resume', methods=['POST'])
def match_resume():
    data = request.get_json()
    job_description = data.get('description', '')

    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400

    if not RESUME_DATA:
        return jsonify({'message': 'No resumes uploaded yet.'}), 200

    cleaned_jd_text = clean_text(job_description)
    jd_skills = extract_skills(cleaned_jd_text)

    results = []

    for filename, resume_data in RESUME_DATA.items():
        score = get_similarity_score(
            cleaned_jd_text,
            resume_data['cleaned_text']
        )

        resume_skills = resume_data['skills']
        matched_skills = list(set(jd_skills) & set(resume_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        results.append({
            'resume_name': filename,
            'match_score': score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'explanation': {
                'job_description_skills': jd_skills,
                'matched_skill_count': len(matched_skills),
                'total_jd_skills': len(jd_skills)
            }
        })

    results.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({
        'message': 'Matching complete',
        'matches': results
    }), 200

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
