import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Le Menteur Pro", page_icon="🃏", layout="wide")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .card {
        display: inline-block;
        width: 80px;
        height: 120px;
        background-color: white;
        border-radius: 10px;
        border: 2px solid #333;
        margin: 5px;
        text-align: center;
        line-height: 120px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
    }
    .card-red { color: #e74c3c; }
    .card-black { color: #2c3e50; }
    .table-zone {
        background-color: #27ae60;
        padding: 40px;
        border-radius: 20px;
        border: 5px solid #1e8449;
        text-align: center;
        min-height: 200px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'main_joueur' not in st.session_state:
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']
    enseignes = {'♠': 'black', '♣': 'black', '♥': 'red', '♦': 'red'}
    st.session_state.deck = [(v, s, enseignes[s]) for v in valeurs for s in enseignes]
    random.shuffle(st.session_state.deck)
    
    st.session_state.main_joueur = [st.session_state.deck.pop() for _ in range(6)]
    st.session_state.main_ia = [st.session_state.deck.pop() for _ in range(6)]
    st.session_state.annonce = None
    st.session_state.pile = []
    st.session_state.tour = "Joueur"

# --- COMPOSANTS GRAPHIQUES ---
def afficher_carte(valeur, icone, couleur, cachee=False):
    if cachee:
        return f'<div class="card" style="background-color: #2c3e50; color: white;">?</div>'
    style = "card-red" if couleur == "red" else "card-black"
    return f'<div class="card {style}">{valeur}{icone}</div>'

# --- INTERFACE ---
st.title("🎭 Le Jeu du Menteur")

# Zone de l'IA (Haut)
st.write(f"### 🤖 IA ({len(st.session_state.main_ia)} cartes)")
ia_html = "".join([afficher_carte("", "", "", cachee=True) for _ in st.session_state.main_ia])
st.markdown(ia_html, unsafe_allow_html=True)

# Zone de Jeu (Milieu)
st.markdown('<div class="table-zone">', unsafe_allow_html=True)
if st.session_state.pile:
    pile_html = "".join([afficher_carte("", "", "", cachee=True) for _ in st.session_state.pile])
    st.markdown(pile_html, unsafe_allow_html=True)
    if st.session_state.annonce:
        st.markdown(f"### Annonce actuelle : {st.session_state.annonce}")
else:
    st.markdown("### La table est vide")
st.markdown('</div>', unsafe_allow_html=True)



# Zone du Joueur (Bas)
st.write("---")
st.write("### 🃏 Votre Main")
main_html = "".join([afficher_carte(v, i, c) for v, i, c in st.session_state.main_joueur])
st.markdown(main_html, unsafe_allow_html=True)

# Contrôles
if st.session_state.tour == "Joueur":
    cols = st.columns([2, 2, 1])
    with cols[0]:
        options = [f"{v}{i}" for v, i, c in st.session_state.main_joueur]
        selection = st.multiselect("Cartes à poser :", options)
    with cols[1]:
        valeur_annonce = st.selectbox("Valeur annoncée :", ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A'])
    with cols[2]:
        if st.button("🚀 Jouer", use_container_width=True):
            if selection:
                # Logique : on retire les objets tuples originaux
                cartes_jouees = [c for c in st.session_state.main_joueur if f"{c[0]}{c[1]}" in selection]
                st.session_state.pile.extend(cartes_jouees)
                st.session_state.main_joueur = [c for c in st.session_state.main_joueur if c not in cartes_jouees]
                st.session_state.annonce = valeur_annonce
                st.session_state.tour = "IA"
                st.rerun()
            
    if st.session_state.annonce:
        if st.button("🚨 MENTEUR !", type="primary"):
            dernieres_cartes = st.session_state.pile[-1:] # Simplifié : on vérifie la dernière pose
            est_mensonge = any(c[0] != st.session_state.annonce for c in dernieres_cartes)
            if est_mensonge:
                st.success("C'était un mensonge ! L'IA ramasse tout.")
                st.session_state.main_ia.extend(st.session_state.pile)
            else:
                st.error("L'IA disait vrai ! Vous ramassez tout.")
                st.session_state.main_joueur.extend(st.session_state.pile)
            st.session_state.pile = []
            st.session_state.annonce = None
            st.rerun()

else:
    # Simulation tour IA
    st.info("L'IA réfléchit...")
    if st.button("Voir le coup de l'IA"):
        # L'IA joue une carte au hasard
        c_ia = st.session_state.main_ia.pop(random.randint(0, len(st.session_state.main_ia)-1))
        st.session_state.pile.append(c_ia)
        st.session_state.annonce = random.choice(['V', 'D', 'R', 'A'])
        st.session_state.tour = "Joueur"
        st.rerun()

# --- VICTOIRE ---
if len(st.session_state.main_joueur) == 0:
    st.balloons()
    st.success("VOUS AVEZ GAGNÉ !")
