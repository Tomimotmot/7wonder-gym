import streamlit as st
st.set_page_config(layout="wide", page_title="7 Wonders Duel")

import json

# Layout: Zeilenweise Karten-IDs (Pyramide: 2–3–4–5–6)
karten_layout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

ressourcen_kürzel = {
    "Holz": "H", "Stein": "S", "Ton": "T", "Papyrus": "P", "Glas": "G"
}

# Karten-Daten laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# Session-State vorbereiten
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

# Klick-Logik über Query-Params
clicked = st.query_params.get("click", [None])[0]
if clicked and clicked.isdigit():
    k_id = int(clicked)
    if k_id not in st.session_state.gezogen:
        st.session_state.gezogen.add(k_id)
        st.session_state.last_reward = karten_data[k_id].get("produziert", "❌ nichts")
    st.query_params.clear()  # URL-Parameter leeren

# CSS Styling
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
    gap: 0.6rem;
}
.card-wrapper {
    all: unset;
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
.leer {
    width: 100px;
    height: 140px;
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Titel
st.markdown("## 🟥 Zeitalter I – Pyramidenlayout (mobilfreundlich & klickbar)")

# Kartenanzeige
st.markdown('<div class="karten-auslage">', unsafe_allow_html=True)

max_karten = max(len(row) for row in karten_layout)

for row in karten_layout:
    row_html = '<div class="reihe">'
    padding = (max_karten - len(row)) // 2
    row_html += '<div class="leer"></div>' * padding

    for karten_id in row:
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen
        rohstoff = karte.get("produziert", "")
        symbol = ressourcen_kürzel.get(rohstoff, "")
        css = "karte gezogen" if gezogen else "karte"

        row_html += f"""
        <form method="get" class="card-wrapper">
          <input type="hidden" name="click" value="{karten_id}"/>
          <button type="submit" class="{css}">
            <div class="kartenressource">{symbol}</div>
            <div class="kartenname">{karte['name']}</div>
          </button>
        </form>
        """

    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Letzter Reward
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset-Button
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen.clear()
    st.session_state.last_reward = None
    st.experimental_rerun()