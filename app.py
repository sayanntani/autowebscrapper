from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from scraper import WebScraper
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_in_production'

scraper = WebScraper()

# Simple in-memory user data (in production use database)
USERS = {}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        username = data.get('username', '').strip()

        if not all([email, password, username]):
            return jsonify({'error': 'All fields required'}), 400

        if email in USERS:
            return jsonify({'error': 'Email already exists'}), 400

        USERS[email] = {
            'password': password,
            'username': username
        }

        return jsonify({'message': 'Registered! Please login.'}), 201

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        if email in USERS and USERS[email]['password'] == password:
            session['user_id'] = email
            session['username'] = USERS[email]['username']
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL required'}), 400

    result = scraper.scrape(url)

    if result['status'] == 'error':
        return jsonify(result), 400

    # Export to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'scrape_{timestamp}.csv'

    try:
        filepath = scraper.export_csv(result, filename)
        result['filename'] = filename
        result['links_count'] = len(result['links'])
        result['images_count'] = len(result['images'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download(filename):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    # Security check
    if '..' in filename or not filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file'}), 400

    filepath = os.path.join('downloads', filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True, host='127.0.0.1', port=5000)
