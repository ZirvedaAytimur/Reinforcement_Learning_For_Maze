import numpy as np
import pygame

n = 6  # number of side squares


def create_maze():
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
    # shortest iteration number to calculate mse

    # parameters to create maze
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

    return n, display_maze, reward, obstacles, states


def act_random(current_position, possible_actions, actions, r):
    if current_position[0] != 0:
        possible_actions.append("up")
    if current_position[0] != n - 1:
        possible_actions.append("down")
    if current_position[1] != 0:
        possible_actions.append("left")
    if current_position[1] != n - 1:
        possible_actions.append("right")
    action = actions[possible_actions[r(0, len(possible_actions) - 1)]]

    return action


# put maze items on screen
def layout(screen_x, screen_y, screen, display_maze, current_position):
    c = 0
    for i in range(0, screen_x, 100):
        for j in range(0, screen_y, 100):
            pygame.draw.rect(screen, (255, 255, 255), (j, i, j + 100, i + 100), 0)
            pygame.draw.rect(screen, display_maze[c], (j + 3, i + 3, j + 95, i + 95), 0)
            c += 1
            pygame.draw.circle(screen, (25, 129, 230), (current_position[1] * 100 + 50, current_position[0] * 100 + 50),
                               30, 0)


shortest_iteration = 10


def calculate_mse(iterations_list):
    # calculating mean squared error
    min_iteration_number = shortest_iteration
    total = 0
    for i in range(len(iterations_list)):
        total += (iterations_list[i] - min_iteration_number) ** 2
    mean_square_error = total / len(iterations_list)

    return mean_square_error


def is_done(current_position):
    if current_position == [n - 1, n - 1]:
        return True


def is_user_exit(run):
    # exit if user choose quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    return run


def move(action, current_position):
    if action == 0:
        current_position[0] -= 1
    elif action == 1:
        current_position[0] += 1
    elif action == 2:
        current_position[1] -= 1
    elif action == 3:
        current_position[1] += 1

    return current_position


def epsilon_greedy(epsilon):
    min_epsilon = 0.05  # min epsilon value
    if epsilon > min_epsilon:
        # increase probability of exploring every step
        epsilon -= 3e-4

    return epsilon
