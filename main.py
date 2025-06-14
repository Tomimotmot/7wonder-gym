import streamlit as st
from env.duel_env import DuelResourceEnv
import logging
import random

# Streamlit Titel
st.title("7 Wonders Duel Simulation")

# Beschreibung der App
st.write("Diese App simuliert eine Runde des Spiels 7 Wonders Duel.")

# Logging Setup (Optional)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("spielverlauf.log"),
        logging.StreamHandler()
    ]
)

# Environment initialisieren
env = DuelResourceEnv(verbose=True)

# Spiel starten
if st.button("Spiel starten"):
    obs = env.reset()
    env.render_board()
    
    ## State
    done = False
    total_reward = 0
    step_counter = 1
    
    # Spielschleife
    while not done:
        # Valid actions zuerst aus Beobachtung holen
        valid_actions = [
            card["id"]
            for card in env.board
            if card["open"] and card["id"] not in env.collected_indices
        ]

        if not valid_actions:
            logging.warning("⚠️ Keine gültigen Aktionen verfügbar.")
            st.warning("Keine gültigen Aktionen verfügbar.")
            break

        action = random.choice(valid_actions)
        obs, reward, done, info = env.step(action)

        karte = info.get("karte", "❌ Ungültig")
        typ = info.get("typ", "-")

        # Ergebnisse in Streamlit anzeigen
        st.write(f"[{step_counter}] Aktion: {karte} ({typ}) → Reward: {reward}")
        total_reward += reward
        step_counter += 1

    st.success(f"✅ Spiel beendet. Gesamt-Reward: {total_reward}")