import re
from urllib.parse import urlparse

def extract_features(url):
    features = []
    
    # --- SAFETY NET START ---
    try:
        url = str(url)
        
        # 1. IP Address
        has_ip = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
        features.append(has_ip)
        
        # 2. URL Length
        if len(url) < 54:
            length_score = 0
        elif len(url) >= 54 and len(url) <= 75:
            length_score = 1
        else:
            length_score = 2
        features.append(length_score)
        
        # 3. @ Symbol
        features.append(1 if "@" in url else 0)
        
        # 4. Redirection //
        last_double_slash = url.rfind('//')
        features.append(1 if last_double_slash > 7 else 0)
        
        # 5. Prefix/Suffix '-'
        parsed = urlparse(url)
        domain = parsed.netloc
        features.append(1 if '-' in domain else 0)
        
        # 6. Sub-Domains
        dot_count = domain.count('.')
        if dot_count <= 2:
            subdomain_score = 0
        elif dot_count == 3:
            subdomain_score = 1
        else:
            subdomain_score = 2
        features.append(subdomain_score)
        
    except Exception:
        # If ANY error happens, return safe zeros to keep training alive
        return [0, 0, 0, 0, 0, 0]
    
    return features