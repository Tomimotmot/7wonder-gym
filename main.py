import streamlit as st
import json

# Muss ganz oben stehen
st.set_page_config(layout="wide", page_title="7 Wonders Duel – Pyramide")

# ----------------------------------------
# Kartenlayout: Zeilen von oben nach unten (2–3–4–5–6 = 20 Karten)
karten_layout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

# Kürzel für Ressourcen
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

# Session State vorbereiten
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

# ----------------------------------------
# Titel
st.markdown("## 🟥 Zeitalter I – Pyramidenlayout (mobilfreundlich & klickbar)")

# Kartenanzeige mit columns
for row in karten_layout:
    cols = st.columns(len(row), gap="small")
    for idx, karten_id in enumerate(row):
        karte = karten_data[karten_id]
        gezogen = karten_id in st.session_state.gezogen
        rohstoff = karte.get("produziert", "")
        symbol = ressourcen_kürzel.get(rohstoff, "")

        with cols[idx]:
            if not gezogen:
                if st.button(f"{karte['name']} ({symbol})", key=f"klick_{karten_id}"):
                    st.session_state.gezogen.add(karten_id)
                    st.session_state.last_reward = rohstoff or "❌ nichts"
            else:
                st.markdown(
                    f"<div style='opacity: 0.3; font-size: 0.85rem; text-align: center;'>"
                    f"<b>{karte['name']}</b><br><small>{symbol}</small></div>",
                    unsafe_allow_html=True
                )

# ----------------------------------------
# Letzter Reward anzeigen
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset-Button
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen.clear()
    st.session_state.last_reward = None
    st.experimental_rerun()