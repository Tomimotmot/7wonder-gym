from env.duel_env import DuelResourceEnv
from stable_baselines3 import PPO

env = DuelResourceEnv()
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)
model.save('ppo_duel_model')