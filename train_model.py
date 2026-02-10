# backend/train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from feature_extractor import extract_features 

# CONFIG
DATASET_FILE = 'dataset.csv'

print("1. Loading Dataset...")
try:
    # Read only needed columns to save memory
    df = pd.read_csv(DATASET_FILE, usecols=['url', 'label'])
    print(f"   Loaded {len(df)} rows.")
except FileNotFoundError:
    print("❌ Error: dataset.csv not found!")
    exit()
except ValueError:
     print("❌ Error: Columns 'url' and 'label' not found. Check your CSV headers!")
     exit()

print("2. Extracting Features for Training (This takes time)...")
# We convert every URL in your CSV into the 6 features
X = []
# Ensure we process them as strings and handle potential missing values
for url in df['url'].astype(str):
    features = extract_features(url)
    X.append(features)

y = df['label'] # 0 or 1

print("3. Training Random Forest Model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KEY CHANGE: class_weight='balanced'
# This tells the model: "Pay extra attention to the minority class (Phishing)!"
clf = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)
clf.fit(X_train, y_train)

# Calculate Accuracy
predictions = clf.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model Trained! Accuracy: {accuracy * 100:.2f}%")

print("4. Saving Model...")
joblib.dump(clf, "phishing_model.pkl")
print("💾 Saved to 'phishing_model.pkl'")