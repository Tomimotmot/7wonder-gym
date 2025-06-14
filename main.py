import streamlit as st
import json

# Kartenlayout: Zeilen von oben nach unten (2–3–4–5–6)
karten_layout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

ressourcen_kürzel = {
    "Holz": "H",
    "Stein": "S",
    "Ton": "T",
    "Papyrus": "P",
    "Glas": "G"
}

# Karten-Daten laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# Session-State initialisieren
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

def karte_ziehen(karten_id):
    st.session_state.gezogen.add(karten_id)
    karte = karten_data[karten_id]
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# CSS-Styling
st.set_page_config(page_title="7 Wonders Duel", layout="wide")
st.markdown("""
<style>
.karten-auslage {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.2rem;
    margin-top: 1rem;
}
.reihe {
    display: flex;
    justify-content: center;
    gap: 0.7rem;
    flex-wrap: nowrap;
}
.karte {
    width: 100px;
    height: 140px;
    border-radius: 8px;
    background-color: #fffdf5;
    border: 2px solid #4caf50;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 6px;
    font-family: sans-serif;
    cursor: pointer;
    transition: transform 0.2s ease;
}
.karte:hover {
    transform: scale(1.03);
}
.gezogen {
    opacity: 0.3;
    pointer-events: none;
}
.kartenressource {
    font-size: 0.85rem;
    font-weight: bold;
    color: #333;
}
.kartenname {
    font-size: 0.72rem;
    font-weight: bold;
    color: #000;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Titel
st.markdown("## 🟥 Zeitalter I – Pyramidenlayout (2–3–4–5–6)")

# Kartenanzeige
st.markdown('<div class="karten-auslage">', unsafe_allow_html=True)
for row in karten_layout:
    st.markdown('<div class="reihe">', unsafe_allow_html=True)
    for karten_id in row:
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen
        rohstoff = karte.get("produziert", "")
        symbol = ressourcen_kürzel.get(rohstoff, "")
        css_classes = ["karte"]
        if gezogen:
            css_classes.append("gezogen")

        with st.form(key=f"karte_{karten_id}"):
            clicked = st.form_submit_button(" ")
            if clicked and not gezogen:
                karte_ziehen(karten_id)

            st.markdown(f"""
                <div class="{' '.join(css_classes)}">
                    <div class="kartenressource">{symbol}</div>
                    <div class="kartenname">{karte['name']}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Letzter Reward
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()

    

