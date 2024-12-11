import json
import logging
import os

from flask import Flask, render_template, request, jsonify, make_response
from werkzeug.utils import secure_filename

import utils

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Secret key for session management (replace with a strong, random key)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Allowed file extensions for uploads (e.g., for privacy policy templates)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

# Upload folder (configure this properly for App Engine)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Example for local dev, adjust for App Engine
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the main configuration page."""
    return render_template('index.html')

@app.route('/generate-gtm-template', methods=['POST'])
def generate_gtm_template():
    """
    Generates GTM templates based on the provided Klaro configuration.
    """
    try:
        klaro_config = request.get_json()

        # Validate the Klaro configuration (add more validation as needed)
        if not utils.validate_klaro_config(klaro_config):
            return jsonify({'error': 'Invalid Klaro configuration'}), 400

        gtm_template = utils.generate_gtm_template_code(klaro_config)
        gtm_trigger = utils.generate_gtm_trigger_code(klaro_config)
        gtm_variable = utils.generate_gtm_variable_code(klaro_config)

        # Create the JSON response
        response_data = {
            'template': gtm_template,
            'trigger': gtm_trigger,
            'variable': gtm_variable,
            'message': 'GTM templates and triggers generated successfully!'
        }

        return jsonify(response_data)

    except Exception as e:
        logging.error(f"Error generating GTM template: {e}")
        return jsonify({'error': 'Failed to generate GTM template'}), 500

@app.route('/simulate-consent', methods=['POST'])
def simulate_consent():
    """Simulates user consent choices for testing."""
    try:
        consent_choices = request.get_json()
        # Implement logic to simulate and test these choices in GTM
        # You might need to use the GTM API or a headless browser for this
        # This is a placeholder for now
        message = f"Simulating consent choices: {consent_choices}"
        logging.info(message)
        return jsonify({'message': message})
    except Exception as e:
        logging.error(f"Error simulating consent: {e}")
        return jsonify({'error': 'Failed to simulate consent'}), 500

@app.route('/upload-policy', methods=['POST'])
def upload_policy():
    """Handles privacy policy template uploads."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the file (e.g., extract text, provide a download link)
        return jsonify({'message': f'File {filename} uploaded successfully'})
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    
@app.route('/download-template')
def download_template():
    """
    Serves a sample privacy policy template file for download.
    """
    try:
        # Replace 'sample_privacy_policy.txt' with the actual filename of your template
        return send_from_directory(
            directory='static/templates', 
            path='sample_privacy_policy.txt', 
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': 'Template file not found'}), 404
    except Exception as e:
        logging.error(f"Error serving template: {e}")
        return jsonify({'error': 'Failed to serve template'}), 500

@app.route('/consent-analytics', methods=['GET'])
def consent_analytics():
    """
    Provides insights into user consent behavior (dummy data for now).
    """
    # In a real application, you would fetch this data from a database
    # where you store consent events.
    dummy_data = {
        'consent_rate': 0.85,
        'rejection_rate': 0.15,
        'popular_choices': {
            'analytics': 0.80,
            'marketing': 0.60,
            'functional': 0.90,
        },
        'consent_over_time': [
            {'date': '2023-10-26', 'consent_rate': 0.75},
            {'date': '2023-10-27', 'consent_rate': 0.80},
            {'date': '2023-10-28', 'consent_rate': 0.85},
        ]
    }
    return jsonify(dummy_data)

if __name__ == '__main__':
    # Use Gunicorn as the WSGI server for production
    if os.environ.get('GAE_ENV') == 'standard':
        app.run() # Gunicorn handles the server
    else:
        # Local development server
        app.run(debug=True, host='127.0.0.1', port=8080)