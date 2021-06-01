import numpy as np
import pygame

n = 8  # number of side squares
maze_number = 1

def create_maze():
    global maze_number
    # Maze
    """
    - States
     - 0 means free
     - -1 means not traversable
     - 1 means goal
    """
    print("Enter 1 or 2 to choose a maze.")
    maze_number = int(input())

    while maze_number != 1 and maze_number != 2:
        print("Enter 1 or 2 to choose a maze.")
        maze_number = int(input())

    if maze_number == 1:
        maze = [[-4, -4, -4, -4, -4, -4, -4, -4],
                [-4, 0, 0, -1, 0, 0, 0, -4],
                [-4, 0, 0, 0, 0, 0, 0, -4],
                [-4, 0, 0, -1, 0, 0, 0, -4],
                [-4, -1, -1, -1, -1, 0, 0, -4],
                [-4, 0, 0, 0, 0, 0, 0, -4],
                [-4, 0, -1, 0, 0, -1, 0, -4],
                [-4, -4, -4, 10, 10, -4, -4, -4]]
    else:
        global n
        n = 10
        maze = [[-4, -4, -4, -4, -4, -4, -4, -4, -4, -4],
                [-4, 0, 0, 0, -1, 0, 0, 0, 0, -4],
                [-4, 0, 0, 0, -1, 0, -1, -1, 0, -4],
                [-4, 0, 0, 0, 0, 0, 0, -1, 0, -4],
                [-4, -1, -1, -1, -1, -1, 0, -1, -1, -4],
                [-4, 0, 0, 0, -1, 0, 0, 0, 0, -4],
                [-4, 0, 0, 0, 0, 0, 0, 0, 0, -4],
                [-4, 0, -1, -1, -1, 0, 0, -1, -1, -4],
                [-4, 0, 0, 0, -1, 0, 0, 0, 0, -4],
                [-4, -4, -4, 10, -4, -4, -4, -4, -4, -4]]
    print(maze)

    # parameters to create maze
    display_maze = [(246, 201, 210) for i in range(n ** 2)]  # displaying background color
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
                display_maze[n * i + j] = (252, 80, 103)
                obstacles.append(n * i + j)
            elif maze[i][j] == -4:
                reward[i, j] = -4
                display_maze[n * i + j] = (198, 13, 13)
                obstacles.append(n * i + j)
            elif maze[i][j] == 10:
                reward[i][j] = 10
                display_maze[n * i + j] = (8, 124, 8)

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
    for i in range(0, screen_x, 70):
        for j in range(0, screen_y, 70):
            pygame.draw.rect(screen, (255, 255, 255), (j, i, j + 100, i + 100), 0)
            pygame.draw.rect(screen, display_maze[c], (j + 3, i + 3, j + 95, i + 95), 0)
            c += 1
            pygame.draw.circle(screen, (25, 129, 230), (current_position[1] * 70 + 35, current_position[0] * 70 + 35),
                               25, 0)



def calculate_mse(iterations_list):
    shortest_iteration = 11
    # calculating mean squared error
    if maze_number == 2:
        shortest_iteration = 20
    min_iteration_number = shortest_iteration
    total = 0
    for i in range(len(iterations_list)):
        total += (iterations_list[i] - min_iteration_number) ** 2
    mean_square_error = total / len(iterations_list)

    return mean_square_error


def is_done(current_position):
    if maze_number == 1:
        if current_position == [n - 1, 3] or current_position == [n - 1, 4]:
            return True
        return False
    elif maze_number == 2:
        if current_position == [n - 1, 3]:
            return True
        return False


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
    min_epsilon = 0.10  # min epsilon value
    if epsilon > min_epsilon:
        # increase probability of exploring every step
        epsilon -= 0.9

    return epsilon
