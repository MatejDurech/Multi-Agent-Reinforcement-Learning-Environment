import random
import numpy as np
from env_Cleaner import EnvCleaner

class MultiAgentQLearning:
    def __init__(self, num_agents, state_size, action_size, learning_rate, discount_factor, epsilon):
        self.num_agents = num_agents
        self.Q = [np.zeros((state_size, action_size)) for _ in range(self.num_agents)]
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def act(self, obs, episode_num):
        actions = []
        for j in range(self.num_agents):
            if np.random.rand() < self.epsilon:
                # Select random action
                actions.append(random.randint(0,(25 * 25 * 4) - 1))
            else:
                # Select action with highest Q-value
                actions.append(np.argmax(self.Q[j][obs[j]]))
        return actions

    def update(self, obs, actions, rewards, next_obs, dones):
        for j in range(self.num_agents):
            # Calculate Q-value for current state and action
            current_q = self.Q[j][obs[j]][actions[j]]

            if dones[j]:
                # Update Q-value for terminal state
                self.Q[j][obs[j]][actions[j]] += self.learning_rate * (rewards[j] - current_q)
            else:
                # Calculate Q-value for next state and best action
                next_q = np.max(self.Q[j][next_obs[j]])
                target_q = rewards[j] + self.discount_factor * next_q

                # Update Q-value for current state and action
                self.Q[j][obs[j]][actions[j]] += self.learning_rate * (target_q - current_q)

if __name__ == '__main__':
    env = EnvCleaner(2, 13, 3)
    num_agents = 2
    state_size = 25 * 25
    action_size = 25 * 25 * 4
    learning_rate = 0.1
    discount_factor = 0.99
    epsilon = 1.0
    max_episodes = 1000

    agent = MultiAgentQLearning(num_agents, state_size, action_size, learning_rate, discount_factor, epsilon)

    for episode in range(max_episodes):
        obs = env.reset()
        done = False
        total_reward = np.zeros(num_agents)

        while not done:
            actions = agent.act(obs, episode)

            next_obs, rewards, dones = env.step(actions)
            total_reward += rewards

            agent.update(obs, actions, rewards, next_obs, dones)

            obs = next_obs
            done = any(dones)

        print(f"Episode: {episode} Total reward: {total_reward} Epsilon: {agent.epsilon}")

        # Decrease epsilon over time
        agent.epsilon = max(0.01, agent.epsilon * 0.99)