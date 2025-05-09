from flask import Flask, render_template, request
from utils.resume_parser import parse_resume
from utils.scorer import score_resume, auto_recommend_role
from utils.job_roles import job_role_skills
from utils.grammar_check import check_grammar
from utils.format_check import check_structure
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            parsed_data = parse_resume(file_path)
            best_role, best_score = auto_recommend_role(parsed_data, job_role_skills)
            mistakes, grammar_suggestions = check_grammar(parsed_data['raw_text'])
            found_sections, missing_sections = check_structure(parsed_data['raw_text'])
            
            return render_template('result.html', 
                                   best_role=best_role,
                                   best_score=best_score,
                                   mistakes=mistakes,
                                   grammar_suggestions=grammar_suggestions,
                                   found_sections=found_sections,
                                   missing_sections=missing_sections,
                                   parsed_data=parsed_data)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)