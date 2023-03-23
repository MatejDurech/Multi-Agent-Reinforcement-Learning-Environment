from env_Cleaner import EnvCleaner
import numpy as np
import random
import time


def changePosToY(width, x, y):
    return (width * y) + x


if __name__ == '__main__':
    width = 9
    env = EnvCleaner(2, width, 6) # [7,5] [7.6]
    num_of_2 = env.numOf2()
    max_iter = 6003
    q = np.zeros((pow(width, 2) * num_of_2, 4))
    print((pow(width, 2) * num_of_2 + 1))
    discount_factor = 0.9
    learning_rate = 0.1
    epsilon = 1.0
    list_of_timesteps = list()
    print(env.occupancy)
    help_time_step = 0

    env.reset()
    state = [1, 1]
    done = False
    timesteps = 0
    reward_xd = 0

    print(env.numOf2())

    for episode in range(max_iter):

        env.reset()
        state = [1, 1]
        done = False
        timesteps = 0
        reward_xd = 0

        while not done:

            # env.render()

            epsilon = 0.05 + (1 - 0.05) * np.exp(-0.0005 * episode)

            state__ = changePosToY(width, state[0], state[1])

            state_ = (state__ * num_of_2 + state__) + env.numOf2()

            if np.random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(q[state_, :])

            next_state, reward, done = env.stepRL(action, 0)

            next_state__ = changePosToY(width, next_state[0], next_state[1])

            next_state_ = (next_state__ * num_of_2 + next_state__) + env.numOf2()

            #if done:
            #    q[state_][action] = q[state_][action] + learning_rate * (reward - q[state_][action])
            #else:
            q[state_][action] = q[state_][action] + learning_rate * (reward + discount_factor * np.max(q[next_state_, :]) - q[state_][action])

            # q[state_][action] = reward + discount_factor * np.max(q[next_state_,:])

            state = next_state

            timesteps += 1
            help_time_step += 1

            reward_xd += reward


        print(epsilon, episode, help_time_step, reward_xd)
        help_time_step = 0
        list_of_timesteps.append(
            f"Training {episode} finished, with epsilon {timesteps:.2f} steps  w reward_xd {reward_xd}")

    for timestep in list_of_timesteps:
        print(timestep)
    print(q)

    env.reset()
    state = [1, 1]
    done = False
    timesteps = 0
    reward_xd = 0

    while not done:
        env.render()

        state__ = changePosToY(width, state[0], state[1])

        state_ = (state__ * num_of_2 + state__) + env.numOf2()

        action = np.argmax(q[state_, :])

        next_state, reward, done = env.stepRL(action, 0)

        next_state__ = changePosToY(width, next_state[0], next_state[1])

        next_state_ = (next_state__ * num_of_2 + next_state__) + env.numOf2()

        state = next_state

        timesteps += 1

        help_time_step += 1

        reward_xd += reward

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
