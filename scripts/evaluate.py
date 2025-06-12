from stable_baselines3 import PPO
from env.duel_env import DuelResourceEnv

env = DuelResourceEnv()
model = PPO.load('ppo_duel_model')

obs = env.reset()
done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    print(f'Action: {action}, Reward: {reward}')