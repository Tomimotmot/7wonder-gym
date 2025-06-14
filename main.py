import streamlit as st
import json
import os

# 👉 Karten-Layout (Index-Matrix wie in DuelResourceEnv)
kartenIndexLayout = [
    [0, 1],
    [2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19]
]

offenLayout = [
    [1, 1],
    [0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1]
]

# 💾 JSON-Datei laden
json_path = os.path.join("data", "grundspiel_karten_zeitalter_1.json")
with open(json_path, "r", encoding="utf-8") as f:
    karten_data = json.load(f)

# 🧠 Session-State initialisieren
if "gezogen" not in st.session_state:
    st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
    st.session_state.last_reward = None

# 💡 Callback-Funktion bei Kartenklick
def karte_ziehen(karten_id):
    karte = karten_data[karten_id]
    st.session_state.gezogen.add(karten_id)
    st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# 🎴 UI – Karten-Auslage
st.title("🎮 Zeitalter I – Kartenkarussell (Streamlit-Version)")

for row_index, reihe in enumerate(kartenIndexLayout):
    cols = st.columns(len(reihe), gap="small")
    for col_index, karten_id in enumerate(reihe):
        karte = karten_data[karten_id]
        offen = offenLayout[row_index][col_index] == 1
        ist_gezogen = karten_id in st.session_state.gezogen

        # 💡 Kartenanzeige (offen oder verdeckt)
        if ist_gezogen:
            with cols[col_index]:
                st.markdown(
                    f"""
                    <div style='opacity: 0.3; text-align: center; font-size: 0.8rem;'>
                        {karte["name"]}
                    </div>
                    """, unsafe_allow_html=True)
        elif offen:
            with cols[col_index]:
                if st.button(f"{karte['name']}", key=f"karte_{karten_id}"):
                    karte_ziehen(karten_id)
                st.markdown(
                    f"<div style='text-align: center; font-size: 0.7rem; color: #555;'>{karte.get('produziert', '')}</div>",
                    unsafe_allow_html=True
                )
        else:
            with cols[col_index]:
                st.button("🂠", key=f"verdeckt_{karten_id}", disabled=True)

# 🎁 Letzter Reward
if st.session_state.last_reward:
    st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# 🔁 Reset Button
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.gezogen = set()
    st.session_state.last_reward = None
    st.experimental_rerun()