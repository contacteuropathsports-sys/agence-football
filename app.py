import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Gestion des imports optionnels
try:
    import gspread
    from google.oauth2.service_account import Credentials
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError:
    pass

# =========================================================
# 1. CONFIGURATION DE LA PAGE
# =========================================================
st.set_page_config(
    page_title="EuroPath Sports - Official App",
    page_icon="⚽",
    layout="centered"
)

# =========================================================
# 2. DESIGN & STYLE (CSS - DARK AGENCY THEME)
# =========================================================
st.markdown("""
    <style>
    /* Fond général */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    
    /* Boutons */
    div.stButton > button {
        background-color: #1E40AF; color: white; border: 1px solid #3B82F6;
        box-shadow: 0px 0px 10px rgba(59, 130, 246, 0.5); font-weight: bold;
    }
    div.stButton > button:hover { background-color: #172554; border-color: #60A5FA; }
    
    /* Titres */
    h1 { color: #60A5FA !important; text-align: center; }
    h2, h3 { color: #E5E7EB !important; }
    
    /* Box Info */
    .info-box {
        text-align: center; background-color: #172554; padding: 15px; 
        border-radius: 10px; border: 1px solid #3B82F6; color: #BFDBFE; margin-bottom: 20px;
    }
    
    /* Carte Stats (Page Démo) */
    .metric-card {
        background-color: #1F2937; border: 1px solid #374151; padding: 20px; 
        border-radius: 10px; text-align: center;
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #60A5FA; }
    .metric-label { font-size: 14px; color: #9CA3AF; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 3. FONCTIONS UTILITAIRES (Le Cerveau)
# =========================================================

def calculer_score(age, budget, division, passeport):
    score = 0
    
    # 1. Budget (Logique CFA/Euro)
    if "Plus de 2500€" in budget: score += 40
    elif "1000€ - 2500€" in budget: score += 20
    
    # 2. Âge (Cœur de cible : 16-21 ans)
    if 16 <= age <= 21: score += 20
    elif 13 <= age < 16: score += 15
    else: score += 5
    
    # 3. Niveau Sportif
    if division == "Académie Pro / D1-D2": score += 30
    elif division == "Club Amateur / Régional": score += 15
    else: score += 5
    
    # 4. Administratif
    if passeport == "Oui": score += 10
    
    return score

def create_radar_chart():
    # Graphique Radar (Demo)
    categories = ['Vitesse', 'Technique', 'Physique', 'Mental', 'Tactique']
    values = [85, 70, 60, 90, 75]
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#1E40AF', alpha=0.25)
    ax.plot(angles, values, color='#3B82F6', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='white')
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#1F2937')
    ax.spines['polar'].set_color('#374151')
    ax.tick_params(axis='x', colors='white')
    return fig

def send_email_alert(player_data):
    try:
        sender_email = st.secrets["email"]["sender"]
        sender_password = st.secrets["email"]["password"]
        receiver_email = "contact.europathsports@gmail.com"
        
        msg = MIMEMultipart()
        msg['From'] = "EuroPath Bot"
        msg['To'] = receiver_email
        msg['Subject'] = f"🔥 PÉPITE : {player_data['Nom']} ({player_data['Score_IA']}/100)"
        
        body = f"Nouveau profil prioritaire !\nNom: {player_data['Nom']}\nVideo: {player_data['Video']}\nBudget: {player_data['Budget']}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception:
        return False

def save_to_google_sheets(data):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("EuroPath_DB").sheet1
        
        row = [
            data["Date"], data["Nom"], data["Email"], data["Telephone"], 
            data["Age"], data["Nationalite"], data["Ville"], data["Poste"], 
            data["Niveau"], data["Budget"], data["Passeport"], data["Video"], 
            data["Score_IA"], data["Statut"]
        ]
        sheet.append_row(row)
        return True
    except Exception:
        # Fallback CSV si Google Sheets n'est pas configuré
        file_path = "candidatures_db.csv"
        header_needed = not os.path.exists(file_path)
        pd.DataFrame([data]).to_csv(file_path, mode='a', header=header_needed, index=False)
        return False

# =========================================================
# 4. NAVIGATION (SIDEBAR)
# =========================================================

# --- LOGO EN HAUT DU MENU ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
elif os.path.exists("logo.jpg"):
    st.sidebar.image("logo.jpg", use_container_width=True)
else:
    # Si pas d'image, on met un titre
    st.sidebar.markdown("<h1 style='text-align: center; color: #60A5FA;'>EuroPath</h1>", unsafe_allow_html=True)

st.sidebar.write("") # Espace

# --- MENU ---
menu = st.sidebar.radio("Navigation", ["📝 Candidature (Scouting)", "🏆 Nos Réussites & Démo"])

st.sidebar.markdown("---")
st.sidebar.info("instagram:\neuropathsports")

# =========================================================
# PAGE 1 : CANDIDATURE (Formulaire)
# =========================================================
if menu == "📝 Candidature (Scouting)":
    
    st.markdown("<h1>EuroPath Sports</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #D97706; font-style: italic; margin-top: -15px; text-align: center;'>« Connecting Talent to Opportunity »</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>🌍 Campagnes de Recrutement 2026 / Scouting Tour</b><br>
        🇪🇸 Espagne | 🇹🇷 Turquie | 🇬🇧 Angleterre
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Dossier de Candidature")

    with st.form("inscription_form"):
        st.markdown("#### 👤 Identité & Contact")
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom complet / Full Name")
            email = st.text_input("Email")
            nationalite = st.text_input("Nationalité")
        with c2:
            age = st.number_input("Âge / Age", 10, 35, 17)
            telephone = st.text_input("WhatsApp (+ Code Pays)")
            ville = st.text_input("Ville & Pays")

        st.divider()

        st.markdown("#### ⚽ Profil Sportif")
        c3, c4 = st.columns(2)
        with c3:
            poste = st.selectbox("Poste", ["Attaquant (FW)", "Milieu Off. (CAM)", "Milieu Déf. (CDM)", "Défenseur Central (CB)", "Latéral (LB/RB)", "Gardien (GK)"])
            club_actuel = st.selectbox("Niveau Actuel", ["Académie Pro / D1-D2", "Club Amateur / Régional", "Quartier / Pas de club"])
        with c4:
            pied = st.radio("Pied Fort", ["Droit", "Gauche", "Ambidextre"], horizontal=True)
            # --- MODIFICATION: VIDEO OPTIONNELLE ---
            video = st.text_input("Lien Vidéo (YouTube/Veo) - (Facultatif / Optional)")

        st.divider()

        st.markdown("#### Financement")
        st.warning("ℹ️ Les frais de dossier sont à votre charge")
        
        # --- BUDGET AVEC CFA ---
        budget_options = [
            "Moins de 500€ (< 330.000 CFA)", 
            "500€ - 1000€ (330.000 - 650.000 CFA)", 
            "1000€ - 2500€ (650.000 - 1.6M CFA)", 
            "Plus de 2500€ (> 1.6M CFA)"
        ]
        
        budget = st.selectbox("Budget Projet (Voyage + Stage)", budget_options)
        passeport = st.radio("Passeport valide ?", ["Oui", "Non"], horizontal=True)
        
        submitted = st.form_submit_button("Envoyer ma Candidature 🚀")

    if submitted:
        # --- MODIFICATION: ON NE VERIFIE PLUS LA VIDEO ICI ---
        if nom and telephone and email:
            score_final = calculer_score(age, budget, club_actuel, passeport)
            statut = "PRIORITAIRE 🔥" if score_final >= 70 else "EN ATTENTE"
            
            nouvelle_candidature = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Nom": nom, "Email": email, "Telephone": telephone, "Age": age,
                "Nationalite": nationalite, "Ville": ville, "Poste": poste,
                "Niveau": club_actuel, "Budget": budget, "Passeport": passeport,
                "Video": video if video else "Non fournie", # Gère le cas vide
                "Score_IA": score_final, "Statut": statut
            }
            
            with st.spinner('Analyse IA et transmission en cours...'):
                save_to_google_sheets(nouvelle_candidature)
                if score_final >= 70:
                    send_email_alert(nouvelle_candidature)
            
            st.success(f"✅ Dossier reçu ! Merci {nom}.")
            
            if score_final >= 70:
                st.balloons()
                st.markdown(f"""
                <div style='background-color: #064E3B; padding: 15px; border-radius: 10px; border: 1px solid #10B981; color: #D1FAE5;'>
                    🌟 <b>PROFIL HAUT POTENTIEL ({score_final}/100)</b><br>
                    Votre profil est éligible à un entretien prioritaire.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Candidature enregistrée. Nous reviendrons vers vous.")
        else:
            st.error("⚠️ Champs manquants : Nom, Email et WhatsApp sont obligatoires.")

# =========================================================
# PAGE 2 : DEMO & REUSSITES
# =========================================================
elif menu == "🏆 Nos Réussites & Démo":
    st.title("Pourquoi choisir EuroPath ?")
    st.markdown("Nous utilisons la Data pour convaincre les clubs européens.")
    
    st.write("")
    col1, col2, col3 = st.columns(3)
    col1.markdown("""<div class="metric-card"><div class="metric-value">150+</div><div class="metric-label">Joueurs Analysés</div></div>""", unsafe_allow_html=True)
    col2.markdown("""<div class="metric-card"><div class="metric-value">5</div><div class="metric-label">Pays Partenaires</div></div>""", unsafe_allow_html=True)
    col3.markdown("""<div class="metric-card"><div class="metric-value">12</div><div class="metric-label">Signatures Pro</div></div>""", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📊 Exemple de Rapport EuroPath")
    d1, d2 = st.columns([1, 1])
    with d1:
        st.markdown("**Joueur :** Mamadou D.")
        st.markdown("**Club Cible :** Valence CF (U19)")
        st.success("✅ **Points Forts détectés :** Mental d'acier, Endurance.")
    with d2:
        fig = create_radar_chart()
        st.pyplot(fig)

# =========================================================
# ADMIN ZONE
# =========================================================
st.sidebar.markdown("---")
with st.sidebar.expander("🔒 Admin Access"):
    password = st.text_input("Password", type="password")
    if password == "Dieuestgrand":
        st.success("Connecté")
        if os.path.exists("candidatures_db.csv"):
            df = pd.read_csv("candidatures_db.csv")
            st.write(df)
            st.download_button("Télécharger CSV", df.to_csv(index=False), "leads.csv")
# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style='text-align: center; color: #6B7280; font-size: 12px; margin-top: 20px;'>
    <p><b>EuroPath Sports Agency</b><br>
    Connecting Talent to Opportunity<br>
    📧 <a href='mailto:contact.europathsports@gmail.com' style='color: #1E3A8A;'>contact.europathsports@gmail.com</a></p>
    <p>© 2026 EuroPath Sports - All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
