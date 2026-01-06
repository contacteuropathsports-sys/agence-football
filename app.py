import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# =========================================================
# 1. CONFIGURATION DE LA PAGE
# =========================================================
st.set_page_config(
    page_title="EuroPath Sports - Official Application",
    page_icon="⚽",
    layout="centered"
)

# =========================================================
# 2. DESIGN & STYLE (CSS - DARK AGENCY THEME)
# =========================================================
st.markdown("""
    <style>
    /* 1. Fond général en mode Sombre (Dark Blue/Black) */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 2. Bouton Envoyer (Bleu Nuit vers Bleu Clair) */
    div.stButton > button {
        background-color: #1E40AF; /* Bleu plus vif */
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 8px;
        width: 100%;
        border: 1px solid #3B82F6; /* Bordure brillante */
        box-shadow: 0px 0px 10px rgba(59, 130, 246, 0.5); /* Effet néon */
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #172554;
        border-color: #60A5FA;
        box-shadow: 0px 0px 20px rgba(96, 165, 250, 0.7);
    }
    
    /* 3. Titres */
    h1 {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        color: #60A5FA !important; /* Bleu clair pour ressortir sur le noir */
        text-shadow: 0px 0px 10px rgba(30, 58, 138, 0.8);
    }
    h2, h3 {
        text-align: center;
        color: #E5E7EB !important; /* Blanc cassé */
    }
    
    /* 4. Encadré d'info (Fond sombre aussi) */
    .info-box {
        text-align: center; 
        background-color: #172554; /* Bleu très foncé */
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #3B82F6;
        color: #BFDBFE;
        margin-bottom: 20px;
    }
    
    /* 5. Inputs (Champs de texte) */
    .stTextInput > div > div > input {
        color: white;
        background-color: #1F2937;
    }
    .stSelectbox > div > div > div {
        color: white;
        background-color: #1F2937;
    }
    </style>
""", unsafe_allow_html=True)
# =========================================================
# 3. ALGORITHME DE SCORING (Le Cerveau)
# =========================================================
def calculer_score(age, budget, division, passeport):
    score = 0
    # 1. Budget (Critère vital)
    if budget == "Plus de 2500€": score += 40
    elif budget == "1000€ - 2500€": score += 20
    
    # 2. Âge (Cœur de cible : 15-19 ans)
    if 15 <= age <= 19: score += 20
    elif 12 <= age < 15: score += 15
    else: score += 5
    
    # 3. Niveau Sportif
    if division == "Académie Pro / D1-D2": score += 30
    elif division == "Club Amateur / Régional": score += 15
    else: score += 5
    
    # 4. Administratif
    if passeport == "Oui": score += 10
    
    return score

# =========================================================
# 4. INTERFACE UTILISATEUR (Frontend)
# =========================================================

# --- HEADER & LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    elif os.path.exists("logo.jpg"): st.image("logo.jpg", use_container_width=True)
    else: st.header("⚽ EuroPath")

st.markdown("<h1>EuroPath Sports</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #D97706; font-style: italic; margin-top: -15px;'>« Connecting Talent to Opportunity »</h3>", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <b>🌍 Campagnes de Recrutement 2026 / Scouting Tour</b><br>
    🇪🇸 Espagne | 🇹🇷 Turquie | 🇬🇧 Angleterre
</div>
""", unsafe_allow_html=True)

# --- FORMULAIRE ---
st.write("")
st.subheader("📝 Dossier de Candidature / Application")

with st.form("inscription_form"):
    
    # Section 1 : Identité
    st.markdown("#### 👤 Identité & Contact")
    c1, c2 = st.columns(2)
    with c1:
        nom = st.text_input("Nom complet / Full Name")
        email = st.text_input("Email")
        nationalite = st.text_input("Nationalité / Nationality")
    with c2:
        age = st.number_input("Âge / Age", 10, 35, 17)
        telephone = st.text_input("WhatsApp (+ Code Pays)")
        ville = st.text_input("Ville & Pays de résidence")

    st.divider()

    # Section 2 : Sportif
    st.markdown("#### ⚽ Profil Sportif / Athletic Profile")
    c3, c4 = st.columns(2)
    with c3:
        poste = st.selectbox("Poste", ["Attaquant (FW)", "Milieu Off. (CAM)", "Milieu Déf. (CDM)", "Défenseur Central (CB)", "Latéral (LB/RB)", "Gardien (GK)"])
        club_actuel = st.selectbox("Niveau Actuel", ["Académie Pro / D1-D2", "Club Amateur / Régional", "Quartier / Pas de club"])
    with c4:
        pied = st.radio("Pied Fort", ["Droit", "Gauche", "Ambidextre"], horizontal=True)
        video = st.text_input("Lien Vidéo (YouTube/Drive)")

    st.divider()

    # Section 3 : Projet
    st.markdown("#### 💰 Financement / Funding")
    st.info("ℹ️ Les frais de voyage et d'académie sont à la charge du joueur. L'agence ne finance pas les essais.")
    
    budget = st.selectbox(
        "Quel est votre budget pour le projet (Voyage + Stage) ?",
        ["Moins de 500€", "500€ - 1000€", "1000€ - 2500€", "Plus de 2500€"]
    )
    passeport = st.radio("Avez-vous un passeport valide ?", ["Oui", "Non"], horizontal=True)
    
    st.write("")
    submitted = st.form_submit_button("Envoyer ma Candidature 🚀")

# =========================================================
# 5. TRAITEMENT DES DONNÉES (Backend)
# =========================================================
if submitted:
    if nom and telephone and email:
        # 1. Calcul
        score_final = calculer_score(age, budget, club_actuel, passeport)
        statut = "PRIORITAIRE" if score_final >= 70 else "EN ATTENTE"
        
        # 2. Création de l'objet
        nouvelle_candidature = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nom": nom,
            "Email": email,
            "Telephone": telephone,
            "Age": age,
            "Nationalite": nationalite,
            "Ville": ville,
            "Poste": poste,
            "Niveau": club_actuel,
            "Budget": budget,
            "Passeport": passeport,
            "Video": video,
            "Score_IA": score_final,
            "Statut": statut
        }
        
        # 3. Sauvegarde CSV (Base de données)
        file_path = "candidatures_db.csv"
        # On écrit l'en-tête seulement si le fichier n'existe pas
        header_needed = not os.path.exists(file_path)
        
        try:
            pd.DataFrame([nouvelle_candidature]).to_csv(file_path, mode='a', header=header_needed, index=False)
            
            # 4. Feedback Utilisateur
            st.success(f"✅ Merci {nom} ! Votre dossier a été transmis à l'équipe EuroPath.")
            
            if score_final >= 70:
                st.balloons()
                st.markdown(f"""
                <div style='background-color: #d1fae5; padding: 10px; border-radius: 5px; border: 1px solid #10b981; color: #065f46;'>
                    🎉 <b>Félicitations !</b> Votre profil a obtenu un <b>Score IA de {score_final}/100</b>.<br>
                    Vous êtes éligible à un entretien prioritaire. Un agent vous contactera sous 24h.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Votre candidature est bien enregistrée dans notre base de talents.")
                
        except Exception as e:
            st.error(f"Erreur technique lors de la sauvegarde : {e}")
            
    else:
        st.error("⚠️ Merci de remplir obligatoirement : Nom, Email et Téléphone.")

# =========================================================
# 6. ZONE ADMIN (Secrète - Pour télécharger les leads)
# =========================================================
st.write("")
st.write("")
st.markdown("---")

# Ce bouton permet de récupérer le fichier CSV généré par le site
if os.path.exists("candidatures_db.csv"):
    with open("candidatures_db.csv", "rb") as file:
        st.download_button(
            label="🔒 Admin: Télécharger la liste des joueurs (.csv)",
            data=file,
            file_name="EuroPath_Leads.csv",
            mime="text/csv"
        )

# =========================================================
# 7. FOOTER
# =========================================================
st.markdown("""
<div style='text-align: center; color: #6B7280; font-size: 12px; margin-top: 20px;'>
    <p><b>EuroPath Sports Agency</b><br>
    Connecting Talent to Opportunity<br>
    📧 <a href='mailto:contact.europathsports@gmail.com' style='color: #1E3A8A;'>contact.europathsports@gmail.com</a></p>
    <p>© 2026 EuroPath Sports - All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
