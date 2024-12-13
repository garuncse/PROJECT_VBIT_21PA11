from flask import Flask, render_template, request, flash, redirect
import httpx
from nlp_utils import detect_emotions, extract_arguments, get_topics
import os
import logging

# Initialize logging for debugging
logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_blog():
    content = None

    # File upload handling
    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        try:
            content = file.read().decode('utf-8', errors='ignore')
        except Exception as e:
            logging.error(f"Error reading uploaded file: {e}")
            flash("Failed to read the uploaded file.", "error")

    # URL handling (if file not provided or invalid)
    if not content and request.form.get('url'):
        url = request.form.get('url')
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            with httpx.Client(timeout=15) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                if 'text/html' in response.headers.get('Content-Type', ''):
                    content = response.text
                else:
                    flash("The URL does not point to valid HTML content.", "error")
        except httpx.RequestError as e:
            logging.error(f"Error fetching URL: {e}")
            flash(f"Failed to retrieve content from the provided URL: {e}", "error")

    # Validate text input if no file or URL content
    if not content and request.form.get('blog_content'):
        content = request.form.get('blog_content')

    # Check if any valid content is provided
    if not content:
        flash("No valid content provided for analysis.", "error")
        return redirect('/')

    # NLP analysis
    try:
        emotions = detect_emotions(content)
        arguments = extract_arguments(content)
        topics = list(get_topics(content))  # Convert to list for template rendering
    except Exception as e:
        logging.error(f"Error during NLP analysis: {e}")
        flash("An error occurred during content analysis. Please try again.", "error")
        return redirect('/')

    return render_template('results.html', topics=topics, emotions=emotions, arguments=arguments)

if __name__ == '__main__':
    app.run(debug=True)
