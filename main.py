from env.duel_env import DuelResourceEnv
import logging
import random




# Environment initialisieren
env = DuelResourceEnv(verbose=True)
obs = env.reset()
env.render_board()

## State
done = False
total_reward = 0
step_counter = 1


# Logging in Datei + Konsole
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("spielverlauf.log"),
        logging.StreamHandler()
    ]
)



# Spielschleife
while not done:
    # Valid actions zuerst aus Beobachtung holen (ab jetzt im Info enthalten)
    valid_actions = [
        card["id"]
        for card in env.board
        if card["open"] and card["id"] not in env.collected_indices
    ]

    if not valid_actions:
        logging.warning("⚠️ Keine gültigen Aktionen verfügbar.")
        break

    action = random.choice(valid_actions)
    obs, reward, done, info = env.step(action)

    karte = info.get("karte", "❌ Ungültig")
    typ = info.get("typ", "-")

    logging.info(f"[{step_counter}] Aktion: {karte} ({typ}) → Reward: {reward}")
    total_reward += reward
    step_counter += 1

print("\n✅ Spiel beendet. Gesamt-Reward:", total_reward)
