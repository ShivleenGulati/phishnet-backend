import pandas as pd
import os


file_1 = 'malicious_phish.csv'
file_2 = 'phishing_site_urls.csv'
file_3 = 'urldata.csv'

def clean_and_normalize(df, filename):
    """
    Standardizes any dataset to just two columns: 'url' and 'label' (0=Safe, 1=Bad)
    """
   
    df.columns = [c.lower().strip() for c in df.columns]
    
    label_col = None
    if 'type' in df.columns: label_col = 'type'
    elif 'label' in df.columns: label_col = 'label'
    elif 'result' in df.columns: label_col = 'result'
    
    if not label_col:
        print(f"  -> Error: Could not find label column in {filename}. Columns are: {list(df.columns)}")
        return None

    url_col = 'url' if 'url' in df.columns else None
    if not url_col:
        print(f"  -> Error: Could not find 'url' column in {filename}")
        return None
        
    df = df[[url_col, label_col]].copy()
    df.columns = ['url', 'label']

    df['label'] = df['label'].astype(str).str.lower().str.strip()
    
    bad_keywords = ['bad', 'phishing', 'malware', 'defacement', '1', 'malicious']
    
    df['label'] = df['label'].apply(lambda x: 1 if x in bad_keywords else 0)
    
    return df

datasets = []

files_to_process = [file_1, file_2, file_3]

print("Starting processing...")

for current_file in files_to_process:
    if os.path.exists(current_file):
        print(f"Reading {current_file}...")
        try:
            raw_df = pd.read_csv(current_file, encoding='utf-8', on_bad_lines='skip', low_memory=False)
            
            clean_df = clean_and_normalize(raw_df, current_file)
            
            if clean_df is not None:
                datasets.append(clean_df)
                print(f"  -> Success! Added {len(clean_df)} URLs.")
        except Exception as e:
            print(f"  -> Failed to read {current_file}. Error: {e}")
    else:
        print(f"  -> File not found: {current_file}")

if datasets:
    print("\nMerging all datasets...")
    final_df = pd.concat(datasets, axis=0)
    
    print(f"Total rows before cleaning: {len(final_df)}")
    
    final_df.drop_duplicates(subset='url', inplace=True)
    
    final_df = final_df.sample(frac=1).reset_index(drop=True)
    
    print(f"Final Count: {len(final_df)} unique URLs")
    
    output_file = 'Final_Combined_Dataset.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\nDONE! Saved to: {output_file}")
else:
    print("\nNo datasets were processed. Check file names.")