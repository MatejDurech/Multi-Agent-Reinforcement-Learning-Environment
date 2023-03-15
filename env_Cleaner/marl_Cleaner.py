from env_Cleaner import EnvCleaner
import numpy as np
import random


def changePosToY(width, x, y):
    return (width * y) + x


if __name__ == '__main__':
    env = EnvCleaner(2, 7, 0)
    max_iter = 4200
    q = np.random.rand(49, 4)
    discount_factor = 0.99
    learning_rate = 0.1
    epsilon = 1
    list_of_timesteps = list()
    for episode in range(max_iter):

        env.reset()
        state = [1, 1]
        done = False
        timesteps = 0
        reward_xd = 0

        while not done:
            # env.render()

            epsilon = 0.05 + (1 - 0.05) * np.exp(-0.001 * episode)

            state_ = changePosToY(7, state[0], state[1])

            if np.random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(q[state_, :])

            next_state, reward, done = env.step(action, 0)

            next_state_ = changePosToY(7, next_state[0], next_state[1])



            if done:
                q[state_][action] = q[state_][action] + learning_rate * (reward - q[state_][action])
            else:
                q[state_][action] = q[state_][action] + learning_rate * (
                        reward + discount_factor * np.max(q[next_state_]) - q[state_][action])

            state = next_state

            timesteps += 1

            reward_xd += reward
        print(episode, timesteps)
        print(q)

        list_of_timesteps.append(
            f"Training {episode} finished, with epsilon {timesteps:.2f} steps  w reward_xd {reward_xd}")

    for timestep in list_of_timesteps:
        print(timestep)
    print(q)
    # print(q)
    # print(changePosToY(4,2,2))
    # print("iter= ", i)
    # env.render()
    # action_list = [random.randint(0, 3), random.randint(0, 3)]
    # reward = env.step(action_list)
    # print('reward', reward)
