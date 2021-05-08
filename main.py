import matplotlib.pyplot as plt

from QLearning import return_QLearning_solution
from SARSA import return_SARSA_solution
from RandomActions import return_randomaction_solution

ql_episodes, ql_cumulative_rewards, ql_iterations, ql_mean_squared_errors = return_QLearning_solution()

sarsa_episodes, sarsa_cumulative_rewards, sarsa_iterations, sarsa_mean_squared_errors = return_SARSA_solution()

ra_episodes, ra_cumulative_rewards, ra_iterations, ra_mean_squared_errors = return_randomaction_solution()

plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
# multiple line plots
plt.plot(ql_episodes, ql_cumulative_rewards, color='blue')
plt.plot(ql_episodes, sarsa_cumulative_rewards, color='red')
plt.plot(ql_episodes, ra_cumulative_rewards, color="green")
plt.title("Cumulative reward for one episode")
plt.xlabel("Episode Number")
plt.ylabel("Cumulative reward")

plt.subplot(2, 2, 2)
# multiple line plots
plt.plot(ql_episodes, ql_iterations, color='blue')
plt.plot(ql_episodes, sarsa_iterations, color='red')
plt.plot(ql_episodes, ra_iterations, color="green")
plt.title("The number of iterations in one episode")
plt.xlabel("Episode Number")
plt.ylabel("Iteration Number")

plt.subplot(2, 2, 3)
# multiple line plots
plt.plot(ql_episodes, ql_mean_squared_errors, color='blue')
plt.plot(ql_episodes, sarsa_mean_squared_errors, color='red')
plt.plot(ql_episodes, ra_mean_squared_errors, color="green")
plt.title("The mean squared error changes")
plt.xlabel("Episode Number")
plt.ylabel("MSE")
plt.legend(["QLearning", "SARSA", "Random"], bbox_to_anchor=(1.05, 1), loc='upper right')

# show graph
plt.show()
