import streamlit as st
import json

# Kartenlayout: Zeilen mit Karten-IDs von oben nach unten
karten_layout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

# Load Karten-Daten
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# Init Session State
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

# Karte ziehen
def karte_ziehen(karten_id):
    karte = karten_data[karten_id]
    st.session_state.gezogen.add(karten_id)
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# Stildefinition (wird nur einmal eingebunden)
st.markdown("""
<style>
.kartenreihe {
    display: flex;
    justify-content: center;
    margin-bottom: 1.2rem;
    gap: 0.5rem;
}
.karte {
    width: 90px;
    height: 130px;
    border-radius: 8px;
    box-shadow: 0 0 5px rgba(0,0,0,0.15);
    font-family: sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 6px;
    text-align: center;
    font-size: 0.75rem;
    cursor: pointer;
}
.offen {
    background-color: #fffdf5;
    border: 2px solid #4caf50;
    color: #000;
}
.verdeckt {
    background-color: #bbb;
    border: 2px solid #888;
    color: transparent;
}
.gezogen {
    opacity: 0.3;
    pointer-events: none;
}
.kartenname {
    font-size: 0.7rem;
    font-weight: bold;
    color: #000;
}
.kartenressource {
    font-size: 0.9rem;
    font-weight: bold;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# Mapping von Rohstoff zu Kürzel
symbol = {
    "Holz": "H",
    "Stein": "S",
    "Ton": "T",
    "Papyrus": "P",
    "Glas": "G"
}

# Karten-Auslage anzeigen
st.title("🎴 Zeitalter I – visuelles 7 Wonders Layout (2–3–4–5–6)")

for row in karten_layout:
    st.markdown('<div class="kartenreihe">', unsafe_allow_html=True)

    for karten_id in row:
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen

        # Ermitteln ob offen oder verdeckt (hier: Regel wie im echten Spiel – abwechselnd)
        offen = True  # Optional: z. B. row_index % 2 == 0 für Wechsel

        klassennamen = ["karte"]
        klassennamen.append("offen" if offen else "verdeckt")
        if gezogen:
            klassennamen.append("gezogen")

        # Inhalt (symbol + name)
        rohstoff = karte.get("produziert", "")
        rohstoff_symbol = symbol.get(rohstoff, "")

        # Karte als klickbarer HTML-Block
        st.markdown(f"""
        <div class="{' '.join(klassennamen)}" onclick="fetch('/?karte={karten_id}', {{method: 'POST'}})">
            <div class="kartenressource">{rohstoff_symbol}</div>
            <div class="kartenname">{karte['name']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Button-Handling in Python
for karten_id in range(len(karten_data)):
    if st.button(f"Ziehe: {karten_data[karten_id]['name']}", key=f"btn_{karten_id}"):
        karte_ziehen(karten_id)

# Letzter Reward
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()