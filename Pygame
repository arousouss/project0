import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Pyramid Scramble",
    page_icon="🎴",
    layout="wide"
)

# --- CLASSES DU JEU ---

class Card:
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = {'PIQUE': '♠', 'COEUR': '♥', 'CARREAU': '♦', 'TREFLE': '♣'}
    SUIT_COLORS = {'PIQUE': 'black', 'COEUR': 'red', 'CARREAU': 'red', 'TREFLE': 'black'}
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = True
    
    def __repr__(self):
        return f"{self.rank}{self.SUITS[self.suit]}"
    
    def get_display(self):
        return f"{self.rank} {self.SUITS[self.suit]}"
    
    def get_color(self):
        return self.SUIT_COLORS[self.suit]
    
    def to_dict(self):
        return {'rank': self.rank, 'suit': self.suit}
    
    @staticmethod
    def from_dict(data):
        return Card(data['rank'], data['suit'])

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS.keys():
            for rank in Card.RANKS:
                self.cards.append(Card(rank, suit))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num_cards):
        dealt_cards = []
        for _ in range(num_cards):
            if self.cards:
                dealt_cards.append(self.cards.pop())
        return dealt_cards
    
    def to_dict(self):
        return [card.to_dict() for card in self.cards]
    
    @staticmethod
    def from_dict(data):
        deck = Deck()
        deck.cards = [Card.from_dict(card_data) for card_data in data]
        return deck

class Hand:
    def __init__(self, player_name="Joueur"):
        self.player_name = player_name
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
        self.sort_hand()
    
    def remove_card(self, card):
        self.cards = [c for c in self.cards if not (c.rank == card.rank and c.suit == card.suit)]
        self.sort_hand()
    
    def sort_hand(self):
        rank_values = {rank: i for i, rank in enumerate(Card.RANKS)}
        suit_values = {suit: i for i, suit in enumerate(Card.SUITS.keys())}
        self.cards.sort(key=lambda card: (suit_values[card.suit], rank_values[card.rank]))
    
    def to_dict(self):
        return [card.to_dict() for card in self.cards]
    
    @staticmethod
    def from_dict(data):
        hand = Hand()
        hand.cards = [Card.from_dict(card_data) for card_data in data]
        return hand

class Pyramid:
    def __init__(self, size=3):
        self.cards = [None] * size
    
    def set_cards(self, new_cards):
        self.cards = new_cards
    
    def replace_card(self, index, new_card):
        if 0 <= index < len(self.cards):
            old_card = self.cards[index]
            self.cards[index] = new_card
            return old_card
        return None
    
    def to_dict(self):
        return [card.to_dict() if card else None for card in self.cards]
    
    @staticmethod
    def from_dict(data):
        pyramid = Pyramid()
        pyramid.cards = [Card.from_dict(card_data) if card_data else None for card_data in data]
        return pyramid

# --- INITIALISATION DE L'ÉTAT DU JEU ---

def init_game():
    """Initialise un nouveau jeu"""
    deck = Deck()
    player_hand = Hand("Joueur 1")
    pyramid = Pyramid(size=3)
    
    # Distribution initiale
    player_hand.cards = deck.deal(5)
    pyramid.set_cards(deck.deal(3))
    
    st.session_state.deck = deck.to_dict()
    st.session_state.discard_pile = []
    st.session_state.player_hand = player_hand.to_dict()
    st.session_state.pyramid = pyramid.to_dict()
    st.session_state.selected_card_index = None
    st.session_state.message = "Choisissez une carte de votre main, puis une carte de la pyramide."
    st.session_state.game_over = False

# Initialisation au premier lancement
if 'deck' not in st.session_state:
    init_game()

# --- FONCTIONS DU JEU ---

def is_valid_move(hand_card, pyramid_card):
    """Vérifie si un coup est valide (même couleur OU même rang)"""
    return hand_card.suit == pyramid_card.suit or hand_card.rank == pyramid_card.rank

def play_card(hand_card_index, pyramid_index):
    """Joue une carte de la main sur la pyramide"""
    player_hand = Hand.from_dict(st.session_state.player_hand)
    pyramid = Pyramid.from_dict(st.session_state.pyramid)
    
    hand_card = player_hand.cards[hand_card_index]
    pyramid_card = pyramid.cards[pyramid_index]
    
    if is_valid_move(hand_card, pyramid_card):
        # Effectue le coup
        old_pyramid_card = pyramid.replace_card(pyramid_index, hand_card)
        player_hand.remove_card(hand_card)
        
        discard_pile = [Card.from_dict(c) for c in st.session_state.discard_pile]
        discard_pile.append(old_pyramid_card)
        
        st.session_state.player_hand = player_hand.to_dict()
        st.session_state.pyramid = pyramid.to_dict()
        st.session_state.discard_pile = [c.to_dict() for c in discard_pile]
        st.session_state.message = "✅ Coup valide ! Continuez à jouer."
        st.session_state.selected_card_index = None
        
        # Vérifie la victoire
        if not player_hand.cards:
            st.session_state.message = "🎉 Félicitations ! Vous avez vidé votre main ! Vous avez gagné !"
            st.session_state.game_over = True
    else:
        st.session_state.message = "❌ Coup invalide. La carte doit correspondre en couleur ou en rang."
        st.session_state.selected_card_index = None

# --- INTERFACE STREAMLIT ---

st.title("🎴 Pyramid Scramble")
st.markdown("---")

# CSS personnalisé pour les cartes
st.markdown("""
<style>
.card {
    border: 3px solid #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    background: white;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    min-width: 90px;
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px auto;
}
.card-selected {
    border: 5px solid #4CAF50;
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.7);
    background: #f0fff0;
}
.card-red {
    color: #d32f2f;
}
.card-black {
    color: #212121;
}
</style>
""", unsafe_allow_html=True)

# Messages et statut
col_msg, col_btn = st.columns([3, 1])
with col_msg:
    if st.session_state.game_over:
        st.success(st.session_state.message)
    else:
        st.info(st.session_state.message)

with col_btn:
    if st.button("🔄 Nouvelle Partie", use_container_width=True):
        init_game()
        st.rerun()

st.markdown("---")

# --- PYRAMIDE ---
st.subheader("🔺 Pyramide")
pyramid_cols = st.columns(3)

pyramid = Pyramid.from_dict(st.session_state.pyramid)

for i, card in enumerate(pyramid.cards):
    with pyramid_cols[i]:
        if card:
            color_class = "red" if card.get_color() == "red" else "black"
            st.markdown(f"<div class='card card-{color_class}'>{card.get_display()}</div>", unsafe_allow_html=True)
            
            if st.session_state.selected_card_index is not None and not st.session_state.game_over:
                if st.button(f"Jouer ici", key=f"pyramid_{i}", use_container_width=True):
                    play_card(st.session_state.selected_card_index, i)
                    st.rerun()

st.markdown("---")

# --- MAIN DU JOUEUR ---
st.subheader("🃏 Votre Main")

player_hand = Hand.from_dict(st.session_state.player_hand)

if player_hand.cards:
    hand_cols = st.columns(len(player_hand.cards))
    
    for i, card in enumerate(player_hand.cards):
        with hand_cols[i]:
            color_class = "red" if card.get_color() == "red" else "black"
            selected_class = "card-selected" if st.session_state.selected_card_index == i else ""
            st.markdown(f"<div class='card card-{color_class} {selected_class}'>{card.get_display()}</div>", unsafe_allow_html=True)
            
            if not st.session_state.game_over:
                button_label = "✓ Sélectionné" if st.session_state.selected_card_index == i else "Sélectionner"
                if st.button(button_label, key=f"hand_{i}", use_container_width=True):
                    st.session_state.selected_card_index = i
                    st.session_state.message = f"Carte sélectionnée : {card}. Cliquez sur une carte de la pyramide."
                    st.rerun()
else:
    st.write("Votre main est vide !")

# --- STATISTIQUES ---
st.markdown("---")
stat_cols = st.columns(3)
with stat_cols[0]:
    st.metric("Cartes en main", len(player_hand.cards))
with stat_cols[1]:
    st.metric("Cartes dans le deck", len(st.session_state.deck))
with stat_cols[2]:
    st.metric("Cartes défaussées", len(st.session_state.discard_pile))

# --- RÈGLES ---
with st.expander("📖 Règles du jeu"):
    st.markdown("""
    **Objectif :** Vider votre main en jouant toutes vos cartes sur la pyramide.
    
    **Comment jouer :**
    1. Sélectionnez une carte de votre main
    2. Cliquez sur une carte de la pyramide pour l'y placer
    3. Votre carte remplacera la carte de la pyramide si elle a la **même couleur** OU le **même rang**
    4. La carte remplacée va dans la défausse
    5. Continuez jusqu'à vider votre main !
    
    **Exemple :**
    - Vous pouvez jouer un 7♠ sur un 7♥ (même rang)
    - Vous pouvez jouer un K♠ sur un A♠ (même couleur)
    """)
