import numpy as np
import pygame
from time import sleep
from random import randint as r
import random
import matplotlib.pyplot as plt

# Maze
"""
- States
 - 0 means free
 - -1 means not traversable
 - 1 means goal
"""
maze = [[0, -1, 0, 0, 0, 0],
        [0, 0, -1, 0, -1, 0],
        [0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 0, 1]]

# parameters to create maze
n = 6  # number of side squares
display_maze = [(160, 160, 160) for i in range(n ** 2)]  # displaying background color
reward = np.zeros((n, n))
obstacles = []  # obstacles in the screen
states = {}  # all states
k = 0  # counter for states
for i in range(n):
    for j in range(n):
        states[(i, j)] = k
        k += 1
        if maze[i][j] == -1:
            reward[i, j] = -1
            display_maze[n * i + j] = (255, 163, 255)
            obstacles.append(n * i + j)
        elif maze[i][j] == 1:
            reward[i, j] = 10
            display_maze[n ** 2 - 1] = (153, 255, 153)

# Q Learning
Q = np.zeros((n ** 2, 4))  # number of states and 4 actions
actions = {"up": 0, "down": 1, "left": 2, "right": 3}  # all actions
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.50   # choose exploit or explore value
min_epsilon = 0.05  # min epsilon value
current_position = [0, 0]


# method to choose an action
def select_an_action(current_state):
    global current_position, epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_position[0] != 0:
            possible_actions.append("up")
        if current_position[0] != n - 1:
            possible_actions.append("down")
        if current_position[1] != 0:
            possible_actions.append("left")
        if current_position[1] != n - 1:
            possible_actions.append("right")
        action = actions[possible_actions[r(0, len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_position[0] != 0:
            possible_actions.append(Q[current_state, 0])
        else:
            possible_actions.append(m - 10)
        if current_position[0] != n - 1:
            possible_actions.append(Q[current_state, 1])
        else:
            possible_actions.append(m - 100)
        if current_position[1] != 0:
            possible_actions.append(Q[current_state, 2])
        else:
            possible_actions.append(m - 100)
        if current_position[1] != n - 1:
            possible_actions.append(Q[current_state, 3])
        else:
            possible_actions.append(m - 100)
        action = random.choice([i for i, a in enumerate(possible_actions) if a == max(possible_actions)])
    return action


# screen parameters
screen_x = n * 100
screen_y = n * 100
screen = pygame.display.set_mode((screen_x, screen_y))


# put maze items on screen
def layout():
    c = 0
    for i in range(0, screen_x, 100):
        for j in range(0, screen_y, 100):
            pygame.draw.rect(screen, (255, 255, 255), (j, i, j + 100, i + 100), 0)
            pygame.draw.rect(screen, display_maze[c], (j + 3, i + 3, j + 95, i + 95), 0)
            c += 1
            pygame.draw.circle(screen, (25, 129, 230), (current_position[1] * 100 + 50, current_position[0] * 100 + 50),
                               30, 0)


# main method
background = (160, 160, 160)  # reset the screen
run = True  # is program running
cumulative_rewards = []  # cumulative rewards for all episodes
cumulative_reward = 0  # cumulative reward for one episode
iterations = []  # number of iterations for all episodes
iteration = 0  # iteration for one episode
episodes = []  # all episodes
episode_number = 0
while run:
    sleep(0.01)
    screen.fill(background)
    layout()

    # exit if user choose quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

    # exit if reach 100 episodes
    if episode_number > 100:
        run = False

    # select action
    current_state = states[(current_position[0], current_position[1])]
    action = select_an_action(current_state)
    if action == 0:
        current_position[0] -= 1
    elif action == 1:
        current_position[0] += 1
    elif action == 2:
        current_position[1] -= 1
    elif action == 3:
        current_position[1] += 1

    # increase cumulative reward and iteration number
    cumulative_reward += reward[current_position[0], current_position[1]]
    iteration += 1

    # update Q table
    new_state = states[(current_position[0], current_position[1])]
    if new_state not in obstacles:
        Q[current_state, action] += alpha * (
                    reward[current_position[0], current_position[1]] + gamma * (np.max(Q[new_state])) - Q[
                current_state, action])
    else:
        Q[current_state, action] += alpha * reward[current_position[0], current_position[1]] - Q[current_state, action]
        current_position = [0, 0]
        if epsilon > min_epsilon:
            # increase probability of exploring every step
            epsilon -= 3e-4

    # if agent reached the goal reset
    if current_position == [n - 1, n - 1]:
        print(f"Episode {episode_number}: final score is {cumulative_reward} with {iteration} iterations")
        current_position = [0, 0]
        iterations.append(iteration)
        cumulative_rewards.append(cumulative_reward)
        episodes.append(episode_number)
        iteration = 0
        cumulative_reward = 0
        episode_number += 1

pygame.quit()
print(Q)

# plot
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.plot(episodes, cumulative_rewards, color="red")
plt.title("Cumulative reward for one episode")
plt.xlabel("Episode Number")
plt.ylabel("Cumulative reward")

plt.subplot(2, 2, 2)
plt.plot(episodes, iterations, color="blue")
plt.title("The number of iterations in one episode")
plt.xlabel("Episode Number")
plt.ylabel("Iteration Number")

plt.show()
