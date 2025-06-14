import streamlit as st
import json
import os

# JSON-Datei laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# Layoutstruktur (Karten-IDs pro Reihe)
karten_layout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

# Offen/verdeckt-Status zu Beginn (wie im echten Spiel)
offen_layout = [
    [1, 1],
    [0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1]
]

# Session State init
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

def karte_ziehen(karten_id):
    karte = karten_data[karten_id]
    st.session_state.gezogen.add(karten_id)
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# Titel
st.title("🎴 Zeitalter I – Original 2-3-4-5-6 Aufbau")

# Karten-Auslage
for row_index, reihe in enumerate(karten_layout):
    offset = (len(karten_layout[-1]) - len(reihe)) // 2
    cols = st.columns(offset + len(reihe))
    for col_index, karten_id in enumerate(reihe):
        karte = karten_data[karten_id]
        offen = offen_layout[row_index][col_index] == 1
        ist_gezogen = karten_id in st.session_state.gezogen

        with cols[offset + col_index]:
            if ist_gezogen:
                st.markdown(f"<div style='opacity: 0.3; text-align: center;'>{karte['name']}</div>", unsafe_allow_html=True)
            elif offen:
                if st.button(f"{karte['name']}", key=f"karte_{karten_id}"):
                    karte_ziehen(karten_id)
                st.markdown(f"<div style='text-align:center; font-size:0.8rem; color:gray'>{karte.get('produziert', '')}</div>", unsafe_allow_html=True)
            else:
                st.button("🂠", key=f"verdeckt_{karten_id}", disabled=True)

# Reward-Anzeige
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()