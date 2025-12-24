import streamlit as st
import random

# Configuration de la page
st.set_page_config(page_title="Quiz Culture Générale", page_icon="📚")

# --- BASE DE DONNÉES DE QUESTIONS ---
# Vous pouvez enrichir cette liste facilement
QUESTIONS = {
    "Histoire": [
        {"q": "Qui était surnommé le Roi-Soleil ?", "o": ["Louis XIV", "Louis XVI", "Napoléon", "Charlemagne"], "r": "Louis XIV"},
        {"q": "En quelle année a eu lieu la chute du mur de Berlin ?", "o": ["1985", "1989", "1991", "1993"], "r": "1989"}
    ],
    "Sciences": [
        {"q": "Quelle est la planète la plus proche du Soleil ?", "o": ["Vénus", "Mars", "Mercure", "Jupiter"], "r": "Mercure"},
        {"q": "Quel est le symbole chimique de l'or ?", "o": ["Ag", "Fe", "Au", "Gd"], "r": "Au"}
    ],
    "Géographie": [
        {"q": "Quelle est la capitale du Japon ?", "o": ["Séoul", "Pékin", "Tokyo", "Bangkok"], "r": "Tokyo"},
        {"q": "Quel fleuve traverse l'Égypte ?", "o": ["Le Nil", "L'Amazone", "Le Congo", "Le Rhin"], "r": "Le Nil"}
    ]
}

# --- INITIALISATION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_actuelle' not in st.session_state:
    st.session_state.question_actuelle = None
if 'repondu' not in st.session_state:
    st.session_state.repondu = False

def nouvelle_question(theme):
    # Sélectionne une question au hasard dans le thème choisi
    liste_questions = QUESTIONS[theme]
    st.session_state.question_actuelle = random.choice(liste_questions)
    st.session_state.repondu = False

# --- INTERFACE ---
st.title("📚 Quiz de Culture Générale")

with st.sidebar:
    st.header("Paramètres")
    theme_choisi = st.selectbox("Choisissez un thème :", list(QUESTIONS.keys()))
    
    if st.button("Nouvelle question 🔄"):
        nouvelle_question(theme_choisi)
    
    st.divider()
    st.write(f"### Score : {st.session_state.score}")
    if st.button("Réinitialiser le score"):
        st.session_state.score = 0
        st.rerun()

# --- ZONE DE JEU ---
if st.session_state.question_actuelle:
    q = st.session_state.question_actuelle
    
    st.info(f"Thème : {theme_choisi}")
    st.subheader(q['q'])
    
    # Affichage des options
    cols = st.columns(2)
    for i, option in enumerate(q['o']):
        with cols[i % 2]:
            if st.button(option, use_container_width=True, disabled=st.session_state.repondu, key=option):
                st.session_state.repondu = True
                if option == q['r']:
                    st.success("✅ Bonne réponse !")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Mauvaise réponse. C'était : {q['r']}")
                st.rerun()
else:
    st.write("Sélectionnez un thème et cliquez sur 'Nouvelle question'.")
