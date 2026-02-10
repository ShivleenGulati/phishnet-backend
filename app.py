# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from database_check import check_database, load_database
from feature_extractor import extract_features

app = Flask(__name__)
CORS(app) 

# --- STARTUP SEQUENCE ---
print("🚀 Starting PHISHNET Server...")

# 1. Load the CSV Database (Layer 1)
load_database("dataset.csv")

# 2. Load the AI Brain (Layer 3)
try:
    model = joblib.load("phishing_model.pkl")
    print("🧠 AI Model loaded successfully.")
except:
    print("❌ Error: 'phishing_model.pkl' not found. Please run train_model.py first!")

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url', '')

    print(f"🔍 Checking: {url}")

    # --- LAYER 1: DATABASE CHECK ---
    # We check the CSV first. If found, we return the answer immediately.
    db_result = check_database(url)
    if db_result:
        return jsonify({
            "result": db_result,
            "source": "Database (Your Combined CSV)",
            "confidence": 100,
            "risk_score": 0 if db_result == "SAFE" else 100
        })

    # --- LAYER 2: HEURISTICS ---
    # Not in CSV? Extract features.
    features = extract_features(url)
    features_array = np.array([features])
    
    # --- LAYER 3: AI MODEL ---
    # Ask the brain.
    # The model gives us two numbers: [Probability of Safe, Probability of Phishing]
    probs = model.predict_proba(features_array)[0]
    prob_safe = probs[0]
    prob_phishing = probs[1]
    
    # LOGIC FIX:
    # If Phishing prob is > 50%, we say PHISHING and use that score.
    # If Phishing prob is < 50% (e.g. 5%), we say SAFE and use the SAFE score (95%).
    
    if prob_phishing > 0.5:
        result = "PHISHING"
        confidence = prob_phishing * 100
    else:
        result = "SAFE"
        confidence = prob_safe * 100
    
    return jsonify({
        "result": result,
        "source": "AI Model (Random Forest)",
        "confidence": round(confidence, 2),
        "risk_score": round(prob_phishing * 100, 2)
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)