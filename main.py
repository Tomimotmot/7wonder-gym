from env.duel_env import DuelResourceEnv

# Environment initialisieren
env = DuelResourceEnv(verbose=True)
obs = env.reset()

done = False
total_reward = 0

# Spielschleife: Agent spielt zufällig
while not done:
    action = env.action_space.sample()  # zufällige Aktion
    obs, reward, done, info = env.step(action)

    # Sicherer Zugriff auf Kartendaten
    karte = info.get("karte", "❌ Ungültig")
    typ = info.get("typ", "-")
    print(f"{karte} ({typ}) → Reward: {reward}")

    total_reward += reward

print("\n✅ Spiel beendet. Gesamt-Reward:", total_reward)
