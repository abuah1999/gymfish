# 1. It renders instances for 500 timesteps, performing random actions.
import gym
env = gym.make('Acrobot-v1')
env.reset()
for _ in range(500):
    env.render()
    env.step(env.action_space.sample())