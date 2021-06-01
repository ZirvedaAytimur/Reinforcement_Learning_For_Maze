import numpy as np
import pygame
from time import sleep
from random import randint as r
import random

from common_functions import create_maze, act_random, layout, calculate_mse, is_done, is_user_exit, move, epsilon_greedy

n, display_maze, reward, obstacles, states = create_maze()

# Q Learning
Q = np.zeros((n ** 2, 4))  # number of states and 4 actions
actions = {"up": 0, "down": 1, "left": 2, "right": 3}  # all actions
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.50  # choose exploit or explore value
current_position = [1, 1]


# method to choose an action
def select_an_action(current_state):
    global current_position, epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        action = act_random(current_position, possible_actions, actions, r)
    else:
        m = np.min(Q[current_state])
        if current_position[0] != 0:
            possible_actions.append(Q[current_state, 0])
        else:
            possible_actions.append(m - 100)
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


screen_x = n * 70
screen_y = n * 70
screen = pygame.display.set_mode((screen_x, screen_y))

# main method
background = (240, 228, 246)  # reset the screen
run = True  # is program running
cumulative_rewards = []  # cumulative rewards for all episodes
cumulative_reward = 0  # cumulative reward for one episode
iterations = []  # number of iterations for all episodes
iteration = 0  # iteration for one episode
episodes = []  # all episodes
mean_squared_errors = []
episode_number = 0
while run:
    sleep(0.01)
    screen.fill(background)
    layout(screen_x, screen_y, screen, display_maze, current_position)

    done = is_done(current_position)

    # if agent reached the goal reset
    if done:
        # print episode result
        print(f"Episode {episode_number}: final score is {cumulative_reward} with {iteration} iterations")

        # add results for plot
        iterations.append(iteration)
        cumulative_rewards.append(cumulative_reward)
        episodes.append(episode_number)

        # calculate mean squared error
        mse = calculate_mse(iterations)
        mean_squared_errors.append(mse)
        print(f"The mean squared error for first {episode_number} episode is: {mse}")

        # reset
        current_position = [1, 1]
        iteration = 0
        cumulative_reward = 0
        episode_number += 1
        done = False

    run = is_user_exit(run)
    pygame.display.flip()

    # exit if reach 100 episodes
    if episode_number > 100:
        run = False

    # select action
    current_state = states[(current_position[0], current_position[1])]
    action = select_an_action(current_state)
    current_position = move(action, current_position)

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
        current_position = [1, 1]

    epsilon = epsilon_greedy(epsilon)

pygame.quit()
print(Q)


def return_QLearning_solution():
    return episodes, cumulative_rewards, iterations, mean_squared_errors
