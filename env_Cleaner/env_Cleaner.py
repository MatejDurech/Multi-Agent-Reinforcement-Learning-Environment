import numpy as np
import maze
import random
import cv2


class EnvCleaner(object):
    def __init__(self, N_agent, map_size, seed):
        self.map_size = map_size
        self.seed = seed
        self.occupancy = self.generate_maze(seed)
        self.N_agent = N_agent
        self.agt_pos_list = []
        self.agt_pos_list.append([1, 1])
        self.agt_pos_list.append([1, 1])

    def generate_maze(self, seed):
        symbols = {
            # default symbols
            'start': 'S',
            'end': 'X',
            'wall_v': '|',
            'wall_h': '-',
            'wall_c': '+',
            'head': '#',
            'tail': 'o',
            'empty': ' '
        }
        maze_obj = maze.Maze(int((self.map_size - 1) / 2), int((self.map_size - 1) / 2), seed, symbols, 1)
        grid_map = maze_obj.to_np()
        for i in range(self.map_size):
            for j in range(self.map_size):
                if grid_map[i][j] == 0:
                    grid_map[i][j] = 2
        return grid_map

    def step(self, action_list, num):
        reward = 0
        next_state = 0
        help_next_sate = 0
        done = False
        if action_list == 0:  # up
            help_next_sate = [self.agt_pos_list[num][0] - 1, self.agt_pos_list[num][1]]
            if self.occupancy[self.agt_pos_list[num][0] - 1][self.agt_pos_list[num][1]] != 1:  # if can move
                self.agt_pos_list[num][0] = self.agt_pos_list[num][0] - 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 1:  # down
            help_next_sate = [self.agt_pos_list[num][0] + 1, self.agt_pos_list[num][1]]
            if self.occupancy[self.agt_pos_list[num][0] + 1][self.agt_pos_list[num][1]] != 1:  # if can move
                self.agt_pos_list[num][0] = self.agt_pos_list[num][0] + 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 2:  # left
            help_next_sate = [self.agt_pos_list[num][0], self.agt_pos_list[num][1] - 1]
            if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1] - 1] != 1:  # if can move
                self.agt_pos_list[num][1] = self.agt_pos_list[num][1] - 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 3:  # right
            help_next_sate = [self.agt_pos_list[num][0], self.agt_pos_list[num][1] + 1]
            if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1] + 1] != 1:  # if can move
                self.agt_pos_list[num][1] = self.agt_pos_list[num][1] + 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] == 0:  # if the spot clear
            reward = -1
        if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] == 0 and \
                self.occupancy[help_next_sate[0]][help_next_sate[1]] == 1:  # if the spot clear
            reward = -5
        if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] == 2:  # if the spot is dirty
            self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] = 0
            reward = 300
        if self.isDone(self.occupancy): done = True
        return next_state, reward, done

    def stepRL(self, action_list, num):
        reward = 0
        next_state = 0
        help_next_sate = 0
        done = False
        if action_list == 2:  # up
            help_next_sate = [self.agt_pos_list[num][0] - 1, self.agt_pos_list[num][1]]
            if self.occupancy[self.agt_pos_list[num][0] - 1][self.agt_pos_list[num][1]] != 1:  # if can move
                self.agt_pos_list[num][0] = self.agt_pos_list[num][0] - 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 3:  # down
            help_next_sate = [self.agt_pos_list[num][0] + 1, self.agt_pos_list[num][1]]
            if self.occupancy[self.agt_pos_list[num][0] + 1][self.agt_pos_list[num][1]] != 1:  # if can move
                self.agt_pos_list[num][0] = self.agt_pos_list[num][0] + 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 0:  # left
            help_next_sate = [self.agt_pos_list[num][0], self.agt_pos_list[num][1] - 1]
            if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1] - 1] != 1:  # if can move
                self.agt_pos_list[num][1] = self.agt_pos_list[num][1] - 1
            next_state = self.agt_pos_list[num]
            # print(next_state)
        if action_list == 1:  # right
            help_next_sate = [self.agt_pos_list[num][0], self.agt_pos_list[num][1] + 1]
            if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1] + 1] != 1:  # if can move
                self.agt_pos_list[num][1] = self.agt_pos_list[num][1] + 1
            next_state = self.agt_pos_list[num]
        if self.occupancy[help_next_sate[0]][help_next_sate[1]] == 1:  # if the spot clear
            reward = -3000
            if self.isDone(self.occupancy): done = True
            return next_state, reward, done
        if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] == 0:  # if the spot clear
            reward = -33
            if self.isDone(self.occupancy): done = True
            return next_state, reward, done
        if self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] == 2:  # if the spot is dirty
            self.occupancy[self.agt_pos_list[num][0]][self.agt_pos_list[num][1]] = 0
            reward = 30
            if self.isDone(self.occupancy): done = True
            return next_state, reward, done


    def get_global_obs(self):
        obs = np.zeros((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.occupancy[i, j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                if self.occupancy[i, j] == 2:
                    obs[i, j, 0] = 0.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 0.0
        for i in range(self.N_agent):
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 0] = 1.0
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 1] = 0.0
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 2] = 0.0
        return obs

    def reset(self):
        self.occupancy = self.generate_maze(self.seed)
        self.agt_pos_list = []
        for i in range(self.N_agent):
            self.agt_pos_list.append([1, 1])

    def render(self):
        obs = self.get_global_obs()
        enlarge = 50
        new_obs = np.ones((self.map_size * enlarge, self.map_size * enlarge, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge),
                                  (0, 0, 0), -1)
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge),
                                  (0, 0, 255), -1)
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge),
                                  (0, 255, 0), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(10)

    def isDone(self, occupancy):
        for row in occupancy:
            if 2 in row:
                return False
        return True

    def numOf2(self):
        num = 0
        for row in self.occupancy:
            for cislo in row:
                if cislo == 2:
                    num += 1
        return num