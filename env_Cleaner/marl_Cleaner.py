from env_Cleaner import EnvCleaner
import numpy as np
import random
import time


def changePosToY(width, x, y):
    return (width * y) + x


if __name__ == '__main__':
    width = 7
    env = EnvCleaner(2, 16)
    num_of_2 = env.numOf2()
    max_iter = 6000

    print(num_of_2)

    #q1 = np.zeros((pow(width, 2), pow(width, 2), num_of_2 + 1, 4))
    #q2 = np.zeros((pow(width, 2), pow(width, 2), num_of_2 + 1, 4))

    q1 = np.zeros((pow(width, 2), pow(width, 2), 4))
    q2 = np.zeros((pow(width, 2), pow(width, 2), 4))

    discount_factor1 = 0.90
    discount_factor2 = 0.90
    learning_rate1 = 0.05
    learning_rate2 = 0.05
    epsilon = 1.0
    list_of_timesteps = list()
    help_time_step = 0

    env.reset()
    state1 = [1, 1]
    state2 = [1, 1]
    done = False
    timesteps = 0
    reward_xd = 0

    for episode in range(max_iter):

        env.reset()
        state1 = [1, 1]
        state2 = [1, 1]
        done = False
        timesteps = 0
        reward_xd = 0
        score = 0

        while not done:

            # env.render()

            epsilon = 0.05 + (1 - 0.05) * np.exp(-0.0005 * episode)

            state1__ = changePosToY(width, state1[0], state1[1])
            state2__ = changePosToY(width, state2[0], state2[1])

            if np.random.uniform(0, 1) < epsilon:
                action1 = random.randint(0, 3)
            else:
                action1 = np.argmax(q1[state1__][state2__])
            if np.random.uniform(0, 1) < epsilon:
                action2 = random.randint(0, 3)
            else:
                action2 = np.argmax(q2[state2__][state1__])

            next_state1, reward1, done = env.stepRL(action1, 0)
            next_state2, reward2, done = env.stepRL(action2, 1)

            #score += reward1 + reward2


            next_state1__ = changePosToY(width, next_state1[0], next_state1[1])
            next_state2__ = changePosToY(width, next_state2[0], next_state2[1])

            if done:
                q1[state1__][state2__][action1] = q1[state1__][state2__][
                                                                    action1] + learning_rate1 * (reward1 -
                                                                                                 q1[state1__][state2__][
                                                                                                     action1])
            else:
                q1[state1__][state2__][action1] = q1[state1__][state2__][
                                                                    action1] + learning_rate1 * (
                                                                        reward1 + discount_factor1 * np.max(
                                                                    q1[next_state1__][next_state2__]) -
                                                                        q1[state1__][state2__][
                                                                            action1])
            if done:
                q2[state2__][state1__][action2] = q2[state2__][state1__][
                                                                    action2] + learning_rate2 * (reward2 -
                                                                                                 q2[state2__][state1__][
                                                                                                     action2])
            else:
                q2[state2__][state1__][action2] = q2[state2__][state1__][
                                                                    action2] + learning_rate2 * (
                                                                        reward2 + discount_factor2 * np.max(
                                                                    q2[next_state2__][next_state1__]) -
                                                                        q2[state2__][state1__][
                                                                            action2])

            state1 = next_state1
            state2 = next_state2

            timesteps += 2
            help_time_step += 2

            reward_xd += reward1

        if episode % 50 == 0:
            print(epsilon, episode, help_time_step / 50, reward_xd)
            help_time_step = 0
        list_of_timesteps.append(
            f"Training {episode} finished, with epsilon {timesteps:.2f} steps  w reward_xd {reward_xd}")

    for timestep in list_of_timesteps:
        print(timestep)

    env.reset()
    state1 = [1, 1]
    state2 = [1, 1]
    done = False
    timesteps = 0
    reward_xd = 0
    help_time_step = 0
    while not done:
        env.render()

        state1__ = changePosToY(width, state1[0], state1[1])
        state2__ = changePosToY(width, state2[0], state2[1])

        action1 = np.argmax(q1[state1__][state2__])

        action2 = np.argmax(q2[state2__][state1__])

        next_state1, reward1, done = env.stepRL(action1, 0)
        next_state2, reward2, done = env.stepRL(action2, 1)

        state1 = next_state1
        state2 = next_state2

        timesteps += 2
        help_time_step += 2

    print(help_time_step)
