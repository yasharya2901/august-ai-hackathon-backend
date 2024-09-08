from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from crewai import Crew, Process
from agents import blood_report_analyst, researcher
from tasks import report_analyze_task, research_task
import logging

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def read_file(primary_path):
    """Reads a file, falls back to another file if the primary file has less than the specified word count."""
    try:
        with open(primary_path, 'r') as f:
            content = f.read()
        
        return content
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return ""

@app.route('/analyze', methods=['POST'])
def analyze_report():
    try:        
        # Extracting the blood report file, city, state, and country from the request
        file = request.files.get('blood_report')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        # Basic validation for required fields
        if not file or not city or not state or not country:
            return jsonify({'error': 'Missing file or location information.'}), 400

        # Saving the uploaded file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Initialize CrewAI with the agents and tasks
        crew = Crew(
            agents=[blood_report_analyst, researcher],
            tasks=[report_analyze_task, research_task],
            process=Process.sequential,
            verbose=True
        )

        # Run the analysis with location inputs
        result = crew.kickoff(inputs={
            'blood_report': file_path,
            'city': city,
            'state': state,
            'country': country
        })
        
        # Read the output files using fallback logic
        analysis = read_file('blood_report_summary12.md')
        recommendations = read_file('blood_report_recommendations12.md')
        specialist_recommendations = read_file('specialists_recommendations12.md')

        # Clean up the uploaded file to maintain a clean environment
        os.remove(file_path)

        return jsonify({
            'analysis': analysis,
            'recommendations': recommendations,
            'specialist_recommendations': specialist_recommendations,
        })
    except Exception as e:
        logging.error(f"An error occurred during report analysis: {e}")
        return jsonify({'error': 'An internal error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
