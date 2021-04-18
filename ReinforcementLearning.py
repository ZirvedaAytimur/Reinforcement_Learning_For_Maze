import gym
import airgym
import numpy as np
import random

env = gym.make('airgym:airsim-drone-sample-v0', ip_address='127.0.0.1', step_length=0.25, image_shape=(84,84,1))

episodes = 50
steps = 20
epsilon_start = 1
epsilon_end = 0.01
epsilon_decay = 200
gamma = 0.9
learning_rate = 0.001
batch_size = 1 #16

episode_rewards = []

for ep in range(episodes):
    ep_reward = 0
    print("Episode {}".format(ep))
    for s in range(steps):
        print("step", s)
        act = env.action_space.sample()
        obs, reward, done, state = env.step(act)
        print("Reward: ", reward)
        print("done: ", done)
        if done:
            break
        ep_reward += reward
        print("Ep_reward: ", ep_reward)
    episode_rewards.append(ep_reward)
    env.reset()