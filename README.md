# IMPLEMENTATION OF REINFORCEMENT LEARNING ALGORITHMS FOR SOLVING MAZE PROBLEM AND COMPARING THE RESULTS

Reinforcement learning enables autonomous robots to learn in various fields. This project is based on an autonomous robot finding the target point in the designed maze. It can be confusing which algorithm to choose in such complex problems. This thesis includes the solution of this maze using Random Actions algorithm, reinforcement learning algorithms QLearning and SARSA and the comparison of the results of the algorithms. The maze prepared with a matrix was visualized with PyGame and the algorithms were coded using Python. Algorithm comparisons were made with how many iterations the robot went to the target point, how many rewards it received, and the mean squared error in each episodes.

Two different mazes were designed for the implementation of the algorithms. Both mazes
were designed in rooms based on the mapping system of robot vacuum cleaners. The first
maze has three rooms and the second maze has four rooms. In both test areas, the starting
point for the robot to start, the target point of the robot was determined, and the boundary
zones with high penalties were drawn to represent the surroundings of the house, the walls
defining the rooms and the obstacles in the rooms were defined with a lower penalty score.
The prize is awarded only when the robot arrives at the designated target point. The algorithm
was created with matrices and visualized later.

You can find the thesis [here](https://github.com/ZirvedaAytimur/Reinforcement_Learning_For_Maze/blob/master/GraduationThesis_2016555006.pdf).

### Results

#### Result of Q-Learning algorithm for The Simpler Maze
https://user-images.githubusercontent.com/46248230/129018935-d8d7259f-143c-44d3-95ee-ba4217cfbe04.mp4

#### Result of SARSA algorithm for The Simpler Maze
https://user-images.githubusercontent.com/46248230/129019169-f298e65f-3b31-4102-a676-e73e1d23d11e.mp4

#### Result of Random Actions for The Simpler Maze
https://user-images.githubusercontent.com/46248230/129019254-e903e826-66d3-4a43-9a43-42c97a4c1d66.mp4

#### Result of Q-Learning algorithm for The Complex Maze
https://user-images.githubusercontent.com/46248230/129019370-84d9c451-0b5f-406e-a9ee-72c6d51b02a3.mp4

#### Result of SARSA algorithm for The Complex Maze
https://user-images.githubusercontent.com/46248230/129019436-da763235-c604-420e-8ddd-a02790ba5554.mp4

#### Result of Random Actions for The Complex Maze
https://user-images.githubusercontent.com/46248230/129019500-7ca28cdf-d7cd-4395-912f-202067fe3e75.mp4
