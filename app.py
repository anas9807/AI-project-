from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pickle
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'cyber-security-project-key'

# --- Match the new 2-Category Mapping from train_model.py ---
# 0: Malware, 1: SQL Injection
# --- Updated to 3 Categories ---
# 0: Malware, 1: SQL Injection, 2: XSS
THREAT_CATEGORIES = ['Malware', 'SQL Injection', 'XSS']

# Load the trained model
try:
    # Adjusted path to match where your train_model.py saves the file
    model_path = 'models/model.pkl' 
    if not os.path.exists(model_path):
        model_path = 'model.pkl' # Fallback to root if not in models/
        
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    MODEL_LOADED = True
    print(f"AI Model loaded successfully from {model_path}!")
except Exception as e:
    MODEL_LOADED = False
    print(f"Warning: model.pkl not found. Running in Demo Mode. Error: {e}")

# Simple user database
USERS = {
    'admin': 'admin123',
    'student': 'cyber123'
}

classification_history = []

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/classify', methods=['POST'])
def classify():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        threat_text = data.get('text', '')
        
        if not threat_text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not MODEL_LOADED:
            # Updated Demo Mode for 2 categories
            threat_text_lower = threat_text.lower()
            if any(word in threat_text_lower for word in ['malware', 'virus', 'exe', 'path']):
                prediction = 0
            elif any(word in threat_text_lower for word in ['sql', 'union', 'select', 'drop']):
                prediction = 1
            else:
                prediction = np.random.randint(0, 2)
            confidence = np.random.uniform(0.70, 0.90)
        else:
            # Actual AI Prediction
            prediction = model.predict([threat_text])[0]
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba([threat_text])[0]
                confidence = float(max(probabilities))
            else:
                confidence = 0.85
        
        # Guard against index errors
        prediction = int(prediction)
        if prediction >= len(THREAT_CATEGORIES):
            prediction = 0 
            
        threat_type = THREAT_CATEGORIES[prediction]
        
        result = {
            'threat_type': threat_type,
            'confidence': round(confidence * 100, 2),
            'text': threat_text[:100] + '...' if len(threat_text) > 100 else threat_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session['username']
        }
        
        classification_history.append(result)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user_history = [h for h in classification_history if h['user'] == session['username']]
    return jsonify(user_history[-10:])

if __name__ == '__main__':
    app.run(debug=True, port=5000)