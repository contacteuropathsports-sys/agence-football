import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random

# --- 1. LA MINE D'OR (Liste des Cibles) ---
# J'ai compilé ici toutes les meilleures sources pour votre agence.
TARGET_URLS = [
    # --- TURQUIE (Priorité Visas Faciles) ---
    "https://www.psgacademyturkey.com/",
    "https://interacademy.inter.it/turkey/",
    "https://noorsports.com/soccer-trial-camps/",    # Très important pour les visas
    "https://www.altinordu.org.tr/en/",              # Le Top niveau turc
    "https://www.soccatours.com/en/turkey/",         # Hub Antalya
    "https://www.alfabesports.com/",
    "https://www.sportscityantalya.com/",

    # --- ESPAGNE (Le Hub Mondial) ---
    "https://siaacademy.com/",
    "https://kaptivasportsacademy.com/",
    "https://www.wospacstages.com/",
    "https://alicantefootballacademy.com/",
    "https://soccerinteraction.com/",
    "https://barcelona-football-academy.com/",
    "https://profutbol.com/",
    
    # --- ANGLETERRE (Prestige) ---
    "https://internationalfootball.academy/",
    "https://fcvinternationalfootballacademy.com/",
    "https://www.ukfootballtrials.com/",
    "https://procademy.co.uk/",
    "https://europasports.net/",
    
    # --- USA (Bourses Universitaires) ---
    "https://www.imgacademy.com/boarding-school/athletics/boys-soccer",
    "https://rushsoccer.com/",
    "https://montverde.org/sports/soccer/",
    
    # --- FRANCE & ITALIE ---
    "https://icef.com/",
    "https://acperugiacalcio.com/academy/",
    "https://www.edusportacademy.com/",
    
    # --- ORGANISATEURS DE DÉTECTIONS ---
    "https://pscsocceracademy.com/",
    "https://ifxsoccer.com/"
]

# --- 2. LES OUTILS DU DATA SCIENTIST ---

def extract_emails_from_text(text):
    """Extrait les emails d'un texte brut via Regex."""
    # Cette regex cherche le motif : texte + @ + texte + . + extension
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    # On utilise set() pour enlever les doublons
    return list(set(emails))

def clean_title(soup):
    """Récupère le titre de la page proprement."""
    if soup.title:
        return soup.title.string.strip()
    return "Titre Inconnu"

# --- 3. LE MOTEUR DE SCRAPING ---

data = []
print(f"🚀 Démarrage du Sourcing Mondial sur {len(TARGET_URLS)} académies...\n")

for url in TARGET_URLS:
    print(f"👉 Analyse de : {url}")
    
    info = {
        "Pays_Estime": "International", # On pourrait affiner plus tard
        "URL": url,
        "Emails": "Non trouvé",
        "Titre_Page": "Inconnu",
        "Status": "Succès"
    }
    
    try:
        # On se fait passer pour un navigateur Chrome Windows pour ne pas être bloqué
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # Requête au site (timeout de 15 secondes max)
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraction des infos
            info["Titre_Page"] = clean_title(soup)
            
            # Analyse du texte complet pour trouver les emails
            text_content = soup.get_text()
            emails_found = extract_emails_from_text(text_content)
            
            if emails_found:
                # On garde les 3 premiers emails trouvés pour que le fichier reste lisible
                info["Emails"] = ", ".join(emails_found[:3])
                print(f"   ✅ Email(s) trouvé(s) : {info['Emails']}")
            else:
                print("   ⚠️  Pas d'email visible direct (chercher sur page Contact).")
        
        else:
            info["Status"] = f"Erreur Code {response.status_code}"
            print(f"   ❌ Erreur accès site : {response.status_code}")
            
    except Exception as e:
        info["Status"] = "Erreur Connection"
        print(f"   ❌ Site inaccessible : {e}")

    # On ajoute le résultat à notre liste
    data.append(info)
    
    # Pause aléatoire entre 1 et 3 secondes (Technique anti-ban)
    time.sleep(random.uniform(1, 3))

# --- 4. SAUVEGARDE ET EXPORT ---

print("\n💾 Sauvegarde des données...")

# Création du DataFrame Pandas
df = pd.DataFrame(data)

# Export Excel
filename = "Lead_Academies_Global_Sourcing.xlsx"
df.to_excel(filename, index=False)

print(f"🎉 Terminé ! Ouvrez le fichier '{filename}' pour voir vos leads.")
