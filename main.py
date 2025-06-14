
import streamlit as st
import json

# Kartenlayout (von oben nach unten → IDs)
karten_layout = [
  [0, 1],                # 2 Karten oben
  [2, 3, 4],             # 3 Karten
  [5, 6, 7, 8],          # 4 Karten
  [9, 10, 11, 12, 13],   # 5 Karten
  [14, 15, 16, 17, 18, 19]  # 6 Karten
]

# Karten-Daten laden
with open("grundspiel_karten_zeitalter_1.json", "r", encoding="utf-8") as f:
  karten_data = json.load(f)

# State-Init
if "gezogen" not in st.session_state:
  st.session_state.gezogen = set()
if "last_reward" not in st.session_state:
  st.session_state.last_reward = None

# Ziehfunktion
def karte_ziehen(karten_id):
  karte = karten_data[karten_id]
  st.session_state.gezogen.add(karten_id)
  st.session_state.last_reward = karte.get("produziert", "❌ nichts")

# Titel
st.title("🎴 Zeitalter I – 2–3–4–5–6 Kartenpyramide (ohne Blockierung)")

# Darstellung der Karten-Auslage
for row in karten_layout:
  cols = st.columns(12)  # Viel Platz für zentriertes Layout
  offset = (12 - len(row)) // 2

  for i, karten_id in enumerate(row):
      karte = karten_data[karten_id]
      gezogen = karten_id in st.session_state.gezogen

      with cols[offset + i]:
          if gezogen:
              st.markdown(f"<div style='opacity: 0.3; text-align:center;'>{karte['name']}</div>", unsafe_allow_html=True)
          else:
              if st.button(karte["name"], key=f"karte_{karten_id}"):
                  karte_ziehen(karten_id)
              st.markdown(
                  f"<div style='text-align:center; font-size:0.8rem; color:gray'>{karte.get('produziert', '')}</div>",
                  unsafe_allow_html=True
              )

# Letzter Reward anzeigen
if st.session_state.last_reward:
  st.markdown(f"### 🎁 Letzter Reward: `{st.session_state.last_reward}`")

# Reset
if st.button("🔄 Spiel zurücksetzen"):
  st.session_state.gezogen = set()
  st.session_state.last_reward = None
  st.experimental_rerun()