# Cyber Threat Intelligence Classification System

A machine learning-powered web application for classifying cyber threats into categories: Malware, XSS and SQL Injection

## 🚀 Features

- **User Authentication** - Secure login system
- **Real-time Classification** - Instant threat classification with confidence scores
- **Classification History** - Track all past classifications
- **Statistics Dashboard** - View threat distribution and analytics
- **Responsive Design** - Works on desktop and mobile devices
- **Modern UI** - Clean, professional interface with dark theme

## 📁 Project Structure

```
/my-cti-project
│
├── app.py              # Flask backend with API routes
├── model.pkl           # Your trained ML model
├── README.md           # This file
│
├── /templates          # HTML templates
│   ├── login.html      # Login page
│   └── dashboard.html  # Main dashboard
│
└── /static             # Static assets
    └── style.css       # Stylesheet
```

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install flask numpy scikit-learn
```

If you're using specific ML libraries for your model, install them too:
```bash
pip install pandas tensorflow torch  # (if needed)
```

### Step 2: Prepare Your Model

Make sure your trained model is saved as `model.pkl` in the project root directory.

If you haven't trained your model yet, here's a basic example:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

# Example training data
X_train = [
    "DDoS flood attack detected",
    "Malware infection in system",
    "XSS vulnerability found",
    "Ransomware encrypted files",
    "SQL injection attempt",
    "Phishing email received"
]
y_train = [0, 1, 2, 3, 4, 5]  # 0=DDoS, 1=Malware, 2=XSS, 3=Ransomware, 4=SQL, 5=Phishing

# Create and train model
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])
model.fit(X_train, y_train)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 👤 Demo Credentials

- **Username:** `demo` | **Password:** `demo123`
- **Username:** `admin` | **Password:** `admin123`

## 🎯 Usage

1. **Login** - Use demo credentials or add your own users
2. **Enter Threat Data** - Type or paste threat information in the text area
3. **Classify** - Click "Classify Threat" button
4. **View Results** - See the threat type and confidence score
5. **Check History** - Review past classifications
6. **View Statistics** - Monitor threat distribution

## 📊 Example Inputs

### Malware
```
Suspicious file detected: trojan.exe attempting to modify system files
```

### XSS (Cross-Site Scripting)
```
<script>alert('XSS')</script> found in user input field
```


### SQL Injection
```
User input: ' OR '1'='1' -- detected in login form
```



## 🔒 Security Notes

⚠️ **For Production Use:**
1. Change the `app.secret_key` in `app.py`
2. Use a proper database (PostgreSQL, MySQL) instead of in-memory storage
3. Hash passwords using bcrypt or similar
4. Add HTTPS/SSL certificate
5. Implement rate limiting
6. Add input validation and sanitization
7. Use environment variables for sensitive data

## 🛠️ Customization

### Adding More Users
Edit the `USERS` dictionary in `app.py`:
```python
USERS = {
    'username': 'admin',
    'newuser': 'admin123'
}
```

### Changing Threat Categories
Modify the `THREAT_CATEGORIES` list in `app.py` and retrain your model accordingly.

### Styling
Edit `static/style.css` to customize colors, fonts, and layout.

## 📝 API Endpoints

- `POST /login` - User authentication
- `GET /logout` - Logout user
- `POST /classify` - Classify threat (JSON: `{"text": "threat data"}`)
- `GET /history` - Get classification history
- `GET /stats` - Get statistics

## 🐛 Troubleshooting

**Model not loading?**
- Ensure `model.pkl` is in the project root
- Check that the model was trained with compatible libraries

**Port 5000 already in use?**
```python
app.run(debug=True, port=5001)  # Change port number
```

**CSS not loading?**
- Check folder structure: `/static/style.css`
- Clear browser cache (Ctrl+Shift+R)

## 📚 Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **ML:** Scikit-learn (or your chosen framework)
- **UI:** Custom CSS with glassmorphism design

## 🎓 For Academic Projects

This project demonstrates:
- Machine Learning classification
- Full-stack web development
- User authentication
- RESTful API design
- Responsive UI/UX design
- Real-time data visualization

## 📄 License

This project is for educational purposes. Feel free to modify and use for your coursework.

## 🤝 Contributing

For improvements or bug fixes, feel free to:
1. Fork the project
2. Create a feature branch
3. Submit a pull request

---

**Created for Academic Project - Cyber Threat Intelligence Classification**


Good luck with your presentation! 🎉
