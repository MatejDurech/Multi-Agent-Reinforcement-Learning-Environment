from env_Cleaner import EnvCleaner
import numpy as np
import random


def changePosToY(width, x, y):
    return (width * y) + x


if __name__ == '__main__':
    env = EnvCleaner(2, 7, 0)
    max_iter = 30
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
        while not done:
            env.render()
            state_ = changePosToY(4, state[0], state[1])

            if np.random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(q[state_, :])

            action_list = [action, action]
            next_state, reward, done = env.step(action_list)
            print(env.step(action_list))

            next_state_ = changePosToY(4, next_state[0], next_state[1])
            print((1 - learning_rate) * q[state_, action] + learning_rate * (
                   reward + discount_factor * np.max(q[next_state_, :])))
            q[state_, action] = (1 - learning_rate) * q[state_, action] + learning_rate * (
                   reward + discount_factor * np.max(q[next_state_, :]))
            state = next_state

            timesteps += 1

            epsilon = 0.1 + (1 - 0.1) * np.exp(-0.1 * episode)

            print(f"Episode {episode} finished, with epsilon {epsilon:.2f}")
            #print(q)
        list_of_timesteps.append(f"Training {episode} finished, with epsilon {timesteps:.2f} steps")

    for timestep in list_of_timesteps:
        print(timestep)
    # print(q)
    # print(changePosToY(4,2,2))
    # print("iter= ", i)
    # env.render()
    # action_list = [random.randint(0, 3), random.randint(0, 3)]
    # reward = env.step(action_list)
    # print('reward', reward)
