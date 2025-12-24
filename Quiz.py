import streamlit as st
import openai
import json

# Configuration de la page
st.set_page_config(page_title="IA Quiz Master", page_icon="🧠")

# --- CONFIGURATION API ---
# Remplacez par votre clé ou utilisez les "secrets" de Streamlit
openai.api_key = "VOTRE_CLE_API_ICI"

# --- INITIALISATION DES VARIABLES DE SESSION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_data' not in st.session_state:
    st.session_state.question_data = None
if 'repondu' not in st.session_state:
    st.session_state.repondu = False

def obtenir_nouvelle_question():
    prompt = (
        "Génère une question de culture générale. "
        "Format JSON strict : {\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"reponse\": \"la bonne option\"}"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.session_state.question_data = json.loads(response.choices[0].message.content)
        st.session_state.repondu = False
    except Exception as e:
        st.error(f"Erreur lors de la génération : {e}")

# --- INTERFACE UTILISATEUR ---
st.title("🧠 IA Quiz Master")
st.write(f"Votre score actuel : **{st.session_state.score}**")

# Bouton pour démarrer ou changer de question
if st.session_state.question_data is None or st.button("Nouvelle question 🔄"):
    obtenir_nouvelle_question()

# Affichage de la question
if st.session_state.question_data:
    q = st.session_state.question_data
    st.subheader(q['question'])
    
    # Création des boutons pour les options
    for option in q['options']:
        if st.button(option, disabled=st.session_state.repondu, key=option):
            st.session_state.repondu = True
            if option == q['reponse']:
                st.success("✅ Bonne réponse !")
                st.session_state.score += 1
            else:
                st.error(f"❌ Mauvaise réponse. C'était : {q['reponse']}")
            st.rerun()

if st.button("Réinitialiser le score 🗑️"):
    st.session_state.score = 0
    st.rerun()
