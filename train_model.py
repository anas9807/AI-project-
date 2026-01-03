import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pickle
import os

# Mapping: 0=Malware, 1=SQLi, 2=XSS
THREAT_CATEGORIES = {0: 'Malware', 1: 'SQL Injection', 2: 'XSS'}

def load_datasets():
    print("Loading and CLEANING datasets...")
    datasets, labels = [], []
    dataset_files = [
        ('datasets/malware.csv', 0),       
        ('datasets/sql1.csv', 1),
        ('datasets/xss.csv', 2) 
    ]
    
    for file_path, label in dataset_files:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
            text_column = next((col for col in df.columns if any(p.lower() in col.lower() for p in ['text', 'payload', 'sentence'])), df.columns[0])

            # --- STEP 1: DROP DUPLICATES ---
            df = df.drop_duplicates(subset=[text_column])

            # Sample a smaller amount to increase variance
            df = df.sample(n=min(len(df), 4000), random_state=42)
            datasets.extend(df[text_column].astype(str).tolist())
            labels.extend([label] * len(df))
            
    return datasets, labels

def train_model(X, y):
    # --- STEP 2: 60% FOR TEST ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60, random_state=42, stratify=y)
    
    # --- STEP 3: LIMIT THE AI ---
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='char',      # Char-level makes it harder than word-level
            ngram_range=(2, 2),   # Simple pairs only
            max_features=300      # FEWER features = More mistakes
        )),
        ('clf', RandomForestClassifier(
            n_estimators=20,      # Fewer trees
            max_depth=3,          # VERY shallow trees (cannot learn everything)
            min_samples_leaf=20,  # Requires many samples to agree
            random_state=42
        ))
    ])
    
    print(f"Training on {len(X_train)} samples... Testing on {len(X_test)} samples...")
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test) * 100
    print(f"\nFinal Test Accuracy: {accuracy:.2f}%")
    
    # --- STEP 4: GENERATE CONFUSION MATRIX ---
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    labels = [THREAT_CATEGORIES[i] for i in range(len(THREAT_CATEGORIES))]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    
    # Using 'Reds' to highlight the errors
    disp.plot(cmap='Reds', values_format='d') 
    plt.title(f'Cyber Threat Classification (Accuracy: {accuracy:.2f}%)')
    
    plt.savefig('confusion_matrix.png')
    print("Confusion Matrix saved as 'confusion_matrix.png'")
    
    return model

if __name__ == "__main__":
    X, y = load_datasets()
    if X:
        model = train_model(X, y)
        if not os.path.exists('models'): os.makedirs('models')
        with open('models/model.pkl', 'wb') as f:
            pickle.dump(model, f)