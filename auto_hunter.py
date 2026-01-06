import pandas as pd
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import time
import random
from datetime import datetime

# --- 1. LE CERVEAU (Mots-clés Dynamiques) ---
SEARCH_QUERIES = [
    'site:instagram.com "football academy" "tryouts 2026" email',
    'site:facebook.com "football trials" "registration" "whatsapp"',
    '"residential soccer academy" "spain" "fees" 2026',
    '"football boarding school" "turkey" "scholarship"',
    'intitle:"application form" "soccer academy" 2026 filetype:pdf',
    '"invitation letter" "football trial" visa'
]

LINKS_PER_QUERY = 10 

# --- 2. LES OUTILS D'ANALYSE ---

def extract_contacts(text):
    emails = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))
    phones = list(set(re.findall(r"\+\d{1,3}\s?\d{6,14}", text)))
    return emails[:2], phones[:2]

def analyze_relevance(text):
    score = 0
    keywords = ["visa", "boarding", "accommodation", "price", "fees", "registration", "scholarship"]
    found_keywords = []
    
    for word in keywords:
        if word in text.lower():
            score += 10
            found_keywords.append(word)
            
    return score, ", ".join(found_keywords)

# --- 3. LE MOTEUR DE CHASSE ---

data = []
print(f"🚀 Lancement du CHASSEUR AUTOMATIQUE ({datetime.now().strftime('%Y-%m-%d')})")

seen_urls = set()

for query in SEARCH_QUERIES:
    print(f"🔎 Recherche Google : '{query}'")
    
    try:
        results = search(query, num_results=LINKS_PER_QUERY, lang="en")
        
        for url in results:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            print(f"   👉 Inspection : {url}")
            
            info = {
                "Date_Discovery": datetime.now().strftime("%Y-%m-%d"),
                "Source_Query": query,
                "URL": url,
                "Title": "Erreur",
                "Emails": "",
                "Phones": "",
                "Relevance_Score": 0,
                "Keywords_Found": ""
            }
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                if url.endswith(".pdf"):
                    info["Title"] = "Fichier PDF (Formulaire probable)"
                    info["Relevance_Score"] = 50
                else:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if soup.title: info["Title"] = soup.title.string.strip()
                        
                        text_content = soup.get_text()
                        emails, phones = extract_contacts(text_content)
                        info["Emails"] = ", ".join(emails)
                        info["Phones"] = ", ".join(phones)
                        
                        score, kws = analyze_relevance(text_content)
                        info["Relevance_Score"] = score
                        info["Keywords_Found"] = kws
                        
                        if score > 0:
                            print(f"      ✅ Pertinent (Score {score}) - Mots: {kws}")
                            if info["Emails"]: print(f"      📧 Email: {info['Emails']}")
                    
            except Exception as e:
                pass
            
            data.append(info)
            time.sleep(random.uniform(2, 5))
            
    except Exception as e:
        print(f"⚠️ Erreur sur la recherche : {e}")
        time.sleep(10)

# --- 4. SAUVEGARDE INTELLIGENTE ---

if not data:
    print("\n🛑 RÉSULTAT : Aucune donnée récupérée.")
    print("👉 Cause probable : Google bloque temporairement vos requêtes (Trop d'appels).")
    print("👉 Solution : Attendez 1h ou changez de connexion (partage de connexion téléphone).")
else:
    df = pd.DataFrame(data)
    
    # On vérifie que la colonne existe avant de trier
    if "Relevance_Score" in df.columns:
        df = df.sort_values(by="Relevance_Score", ascending=False)
    
    filename = f"Chasse_Offres_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)
    
    print(f"\n🎉 Terminé ! {len(data)} opportunités trouvées.")
    print(f"Ouvrez le fichier '{filename}' pour voir les résultats.")
