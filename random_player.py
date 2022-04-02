#import gym
from oned_chess import OneDChessEnvironment

env = OneDChessEnvironment()
env.reset()
done = False
while (not done):
    env.render()
    _,_,done,_ = env.step(env.action_space.sample())