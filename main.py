import streamlit as st
from env.duel_env import DuelResourceEnv
import random

# Titel
st.title("🎮 7 Wonders Duel – KI-Zug-Simulation")

# Environment initialisieren
env = DuelResourceEnv(verbose=True)
obs = env.reset()

# Karten-Stapel anzeigen
st.subheader("🔹 Kartenstapel anzeigen")

# Optional: Wenn render_board() ein Text-Board zurückgibt
try:
    board_output = env.render_board()
    if board_output:
        st.text(board_output)
except Exception as e:
    st.warning(f"Board konnte nicht angezeigt werden: {e}")

# Spielstatus
done = False
total_reward = 0
step_counter = 1
log_buffer = []

# Spielschleife
while not done:
    # Gültige Aktionen bestimmen
    valid_actions = [
        card["id"]
        for card in env.board
        if card["open"] and card["id"] not in env.collected_indices
    ]

    if not valid_actions:
        st.warning("⚠️ Keine gültigen Aktionen mehr verfügbar.")
        break

    # Zufällige gültige Aktion wählen
    action = random.choice(valid_actions)
    obs, reward, done, info = env.step(action)

    # Infos extrahieren
    karte = info.get("karte", "❌ Ungültig")
    typ = info.get("typ", "-")
    zug_info = f"[{step_counter}] Aktion: {karte} ({typ}) → Reward: {reward}"
    log_buffer.append(zug_info)
    step_counter += 1
    total_reward += reward

# Ergebnisse anzeigen
st.success(f"✅ Spiel beendet. Gesamt-Reward: {total_reward}")

# Spielverlauf anzeigen
st.subheader("📜 Spielverlauf")
for line in log_buffer:
    st.text(line)