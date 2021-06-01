import pygame
from time import sleep
from random import randint as r

from common_functions import create_maze, act_random, layout, calculate_mse, is_done, is_user_exit, move

n, display_maze, reward, obstacles, states = create_maze()

actions = {"up": 0, "down": 1, "left": 2, "right": 3}  # all actions
current_position = [1, 1]


# method to choose an action
def select_an_action(current_state):
    global current_position
    possible_actions = []
    action = act_random(current_position, possible_actions, actions, r)
    return action


# screen parameters
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
    if done or iteration == 20000:
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

    new_state = states[(current_position[0], current_position[1])]
    if new_state in obstacles:
        current_position = [1, 1]

pygame.quit()


def return_randomaction_solution():
    return episodes, cumulative_rewards, iterations, mean_squared_errors
