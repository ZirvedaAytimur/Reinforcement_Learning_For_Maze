import gym
import airgym

env = gym.make('airgym:airsim-drone-sample-v0',ip_address='127.0.0.1',step_length=0.25, image_shape=(608,608,3))

episodes = 10
steps = 20
episode_rewards = []
for ep in range(episodes):
    ep_reward = 0
    print("Episode {}".format(ep))
    for s in range(steps):
        act = env.action_space.sample()
        obs, reward, done, state = env.step(act)
        ep_reward += reward
        if done:
            break
    episode_rewards.append(ep_reward)
    env.reset()
