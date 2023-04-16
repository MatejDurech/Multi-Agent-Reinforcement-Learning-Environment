from env import Env
import numpy as np
import random
import time
import matplotlib.pyplot as plt


class MARL:
    def changePosToNumber(self, width, x, y):
        return (width * y) + x

    def graph(self, x, y):
        plt.plot(x, y)
        plt.xlabel('Epizóda')
        plt.ylabel('Počet krokov v epizóde')
        plt.title('Mapa číslo 6')
        plt.show()

    def createQtable(self, width):
        return np.zeros((pow(width, 2), pow(width, 2), 4))

    def policy(self, epsilon, q1, q2, state1__, state2__):
        if np.random.uniform(0, 1) < epsilon:
            action1 = random.randint(0, 3)
        else:
            action1 = np.argmax(q1[state1__][state2__])
        if np.random.uniform(0, 1) < epsilon:
            action2 = random.randint(0, 3)
        else:
            action2 = np.argmax(q2[state2__][state1__])

        return action1, action2

    def updateQtable(self, done, q1, q2, state1__, state2__, action1, action2, learning_rate1, learning_rate2, reward1,
                     reward2, discount_factor1, discount_factor2, next_state1__, next_state2__):
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

    def training(self, env):
        width = 7
        max_iter = 6000

        q1 = self.createQtable(width)
        q2 = self.createQtable(width)

        discount_factor1 = 0.90
        discount_factor2 = 0.90
        learning_rate1 = 0.05
        learning_rate2 = 0.05
        epsilon = 1.0
        x = list()
        y = list()

        for episode in range(max_iter):

            env.reset()
            help_time_step = 0
            state1 = [1, 1]
            state2 = [1, 1]
            done = False

            while not done:
                epsilon = 0.05 + (1 - 0.05) * np.exp(-0.0005 * episode)

                state1__ = self.changePosToNumber(width, state1[0], state1[1])
                state2__ = self.changePosToNumber(width, state2[0], state2[1])

                action1, action2 = self.policy(epsilon, q1, q2, state1__, state2__)

                next_state1, reward1, done = env.stepRL(action1, 0)
                next_state2, reward2, done = env.stepRL(action2, 1)

                next_state1__ = self.changePosToNumber(width, next_state1[0], next_state1[1])
                next_state2__ = self.changePosToNumber(width, next_state2[0], next_state2[1])

                self.updateQtable(done, q1, q2, state1__, state2__, action1, action2, learning_rate1, learning_rate2,
                                  reward1, reward2, discount_factor1, discount_factor2, next_state1__, next_state2__)

                state1 = next_state1
                state2 = next_state2

                help_time_step += 2

            if episode % 10 == 0 and episode != 0:
                x.append(episode)
                y.append(help_time_step)

            print(episode)

            if episode == 0:
                print("bulo to takoj:", help_time_step)

            # if episode % 50 == 0 and episode != 0:
            #    print(epsilon, episode, help_time_step / 50, reward_xd)
            #    help_time_step = 0

            #list_of_timesteps.append(f"Training {episode} finished, with epsilon {timesteps:.2f} steps  w reward_xd {reward_xd}")

        self.graph(x, y)
        return q1, q2

    def run(self, env, q1, q2):
        width = 7
        state1 = [1, 1]
        state2 = [1, 1]
        done = False
        timesteps = 0
        reward_xd = 0
        help_time_step = 0
        while not done:
            env.render()

            state1__ = self.changePosToNumber(width, state1[0], state1[1])
            state2__ = self.changePosToNumber(width, state2[0], state2[1])

            action1 = np.argmax(q1[state1__][state2__])

            action2 = np.argmax(q2[state2__][state1__])

            next_state1, reward1, done = env.stepRL(action1, 0)
            next_state2, reward2, done = env.stepRL(action2, 1)

            state1 = next_state1
            state2 = next_state2

            timesteps += 2
            help_time_step += 2

        print(help_time_step)
