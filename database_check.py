# backend/database_check.py
import pandas as pd
import os

# Global variable to store our "Lookup Table"
URL_DATABASE = {}

def load_database(csv_filepath):
    """
    Loads the CSV file into a Python Dictionary for instant lookup.
    """
    global URL_DATABASE
    
    if not os.path.exists(csv_filepath):
        print(f"⚠️ Warning: {csv_filepath} not found. Layer 1 will be empty.")
        return

    print(f"📂 Loading Database from {csv_filepath}...")
    
    try:
        # Load only the necessary columns to save memory
        # CHANGE 'url' and 'label' to match your CSV headers exactly!
        # dtype={'url': str, 'label': int} ensures data is read correctly
        df = pd.read_csv(csv_filepath, usecols=['url', 'label'], dtype={'url': str, 'label': int})
        
        # Convert to dictionary: { 'google.com': 0, 'badsite.com': 1 }
        # This makes checking a URL instant (O(1) time complexity)
        URL_DATABASE = dict(zip(df['url'], df['label']))
        
        print(f"✅ Database Loaded! Contains {len(URL_DATABASE)} known sites.")
        
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        print("💡 Tip: Check if your CSV columns are named 'url' and 'label'")

def check_database(url):
    """
    Checks if the URL exists in our CSV.
    Returns: 'SAFE', 'PHISHING', or None.
    """
    # Check if the exact URL is in our dictionary
    if url in URL_DATABASE:
        label = URL_DATABASE[url]
        # 0 = Safe, 1 = Phishing (Adjust based on your dataset!)
        if label == 0: 
            return "SAFE"
        elif label == 1:
            return "PHISHING"
            
    # If not found, return None so Layer 2 & 3 can take over
    return None