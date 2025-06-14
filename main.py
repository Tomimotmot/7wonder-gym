import streamlit as st
import json

# ----------------------------------------
# Kartenlayout: Zeilen von oben nach unten (2–3–4–5–6 = 20 Karten)
karten_layout = [
    [0, 1],                      # 2 Karten oben
    [2, 3, 4],                   # 3 Karten
    [5, 6, 7, 8],                # 4 Karten
    [9, 10, 11, 12, 13],         # 5 Karten
    [14, 15, 16, 17, 18, 19]     # 6 Karten unten
]

# Rohstoff-Symbole (Initialen)
ressourcen_kürzel = {
    "Holz": "H",
    "Stein": "S",
    "Ton": "T",
    "Papyrus": "P",
    "Glas": "G"
}

# ----------------------------------------
# Karten-Daten laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# ----------------------------------------
# Session State
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

# Karte ziehen
def karte_ziehen(karten_id):
    st.session_state.gezogen.add(karten_id)
    karte = karten_data[karten_id]
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# ----------------------------------------
# CSS-Styling
st.markdown("""
<style>
.kartenreihe {
    display: flex;
    justify-content: center;
    margin-bottom: 1.2rem;
    gap: 0.6rem;
}
.karte {
    width: 100px;
    height: 140px;
    border-radius: 8px;
    box-shadow: 0 0 5px rgba(0,0,0,0.15);
    font-family: sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 6px;
    text-align: center;
    font-size: 0.75rem;
}
.offen {
    background-color: #fffdf5;
    border: 2px solid #4caf50;
    color: #000;
    cursor: pointer;
}
.gezogen {
    opacity: 0.3;
    pointer-events: none;
}
.kartenname {
    font-size: 0.72rem;
    font-weight: bold;
    color: #000;
    margin-bottom: 3px;
}
.kartenressource {
    font-size: 0.85rem;
    font-weight: bold;
    color: #333;
    margin-top: 3px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Titel
st.markdown("## 🟥 Zeitalter I – Kartenpyramide (2–3–4–5–6)")

# ----------------------------------------
# Kartenanzeige
for row in karten_layout:
    num_cards = len(row)
    total_slots = 12
    padding = (total_slots - num_cards) // 2
    cols = st.columns(total_slots, gap="small")

    for i, karten_id in enumerate(row):
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen
        rohstoff = karte.get("produziert", "")
        symbol = ressourcen_kürzel.get(rohstoff, "")
        klassennamen = ["karte", "offen"]
        if gezogen:
            klassennamen.append("gezogen")

        with cols[padding + i]:
            if not gezogen:
                if st.button(" ", key=f"karte_{karten_id}"):
                    karte_ziehen(karten_id)

            st.markdown(f"""
            <div class="{' '.join(klassennamen)}">
                <div class="kartenressource">{symbol}</div>
                <div class="kartenname">{karte['name']}</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------
# Reward & Reset
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()
        