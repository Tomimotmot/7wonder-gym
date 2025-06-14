import streamlit as st
import json

# ----------------------------------------
# Kartenlayout: Zeilen von oben nach unten (2-3-4-5-6 Karten = 20 Karten)
karten_layout = [
    [0, 1],                      # Reihe 0 (oben)
    [2, 3, 4],                   # Reihe 1
    [5, 6, 7, 8],                # Reihe 2
    [9, 10, 11, 12, 13],         # Reihe 3
    [14, 15, 16, 17, 18, 19]     # Reihe 4 (unten)
]

# Mapping: Rohstoffsymbol
ressourcen_kürzel = {
    "Holz": "H",
    "Stein": "S",
    "Ton": "T",
    "Papyrus": "P",
    "Glas": "G"
}

# ----------------------------------------
# JSON-Daten laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# ----------------------------------------
# Session-State initialisieren
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

def karte_ziehen(karten_id):
    karte = karten_data[karten_id]
    st.session_state.gezogen.add(karten_id)
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# ----------------------------------------
# Stildefinition einmalig einbinden
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
.verdeckt {
    background-color: #bbb;
    border: 2px solid #888;
    color: transparent;
    cursor: default;
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
# Anzeige
st.title("🎴 Zeitalter I – Kartenpyramide (2–3–4–5–6)")

# Karten anzeigen – jede Reihe zentriert
for row in karten_layout:
    st.markdown('<div class="kartenreihe">', unsafe_allow_html=True)
    for karten_id in row:
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen

        # Anzeige vorbereiten
        rohstoff = karte.get("produziert", "")
        symbol = ressourcen_kürzel.get(rohstoff, "")
        klassennamen = ["karte", "offen"]
        if gezogen:
            klassennamen.append("gezogen")

        # HTML-Ausgabe pro Karte
        if gezogen:
            st.markdown(f"""
            <div class="{' '.join(klassennamen)}">
                <div class="kartenressource">{symbol}</div>
                <div class="kartenname">{karte['name']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Jede Karte bekommt einen eigenen Button
            if st.button(f"{karte['name']}", key=f"karte_{karten_id}"):
                karte_ziehen(karten_id)

            # Danach nochmal als gestylter Kasten anzeigen
            st.markdown(f"""
            <div class="{' '.join(klassennamen)}">
                <div class="kartenressource">{symbol}</div>
                <div class="kartenname">{karte['name']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------
# Letzter Reward
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# ----------------------------------------
# Reset-Button
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()