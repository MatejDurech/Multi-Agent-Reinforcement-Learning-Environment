import numpy as np
import maze
import random
import cv2


class EnvCleaner(object):
    def __init__(self, N_agent, seed):
        self.map_size = 7
        self.seed = seed
        self.grid = self.generate_maze(seed)
        self.N_agent = N_agent
        self.agents = []
        self.agents.append([1, 1])
        self.agents.append([1, 1])

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
        done = False
        if action_list == 0:
            if self.grid[self.agents[num][0] - 1][self.agents[num][1]] != 1:
                self.agents[num][0] = self.agents[num][0] - 1
        if action_list == 1:
            if self.grid[self.agents[num][0] + 1][self.agents[num][1]] != 1:
                self.agents[num][0] = self.agents[num][0] + 1
        if action_list == 2:
            if self.grid[self.agents[num][0]][self.agents[num][1] - 1] != 1:
                self.agents[num][1] = self.agents[num][1] - 1
        if action_list == 3:
            if self.grid[self.agents[num][0]][self.agents[num][1] + 1] != 1:
                self.agents[num][1] = self.agents[num][1] + 1
        if self.grid[self.agents[num][0]][self.agents[num][1]] == 2:
            self.grid[self.agents[num][0]][self.agents[num][1]] = 0
        if self.isDone(self.grid): done = True
        return done

    def stepRL(self, action_list, num):
        reward = 0
        next_state = 0
        help_next_sate = 0
        done = False
        if action_list == 2:
            help_next_sate = [self.agents[num][0] - 1, self.agents[num][1]]
            if self.grid[self.agents[num][0] - 1][self.agents[num][1]] != 1:
                self.agents[num][0] = self.agents[num][0] - 1
            next_state = self.agents[num]
        if action_list == 3:
            help_next_sate = [self.agents[num][0] + 1, self.agents[num][1]]
            if self.grid[self.agents[num][0] + 1][self.agents[num][1]] != 1:
                self.agents[num][0] = self.agents[num][0] + 1
            next_state = self.agents[num]
        if action_list == 0:
            help_next_sate = [self.agents[num][0], self.agents[num][1] - 1]
            if self.grid[self.agents[num][0]][self.agents[num][1] - 1] != 1:
                self.agents[num][1] = self.agents[num][1] - 1
            next_state = self.agents[num]
        if action_list == 1:
            help_next_sate = [self.agents[num][0], self.agents[num][1] + 1]
            if self.grid[self.agents[num][0]][self.agents[num][1] + 1] != 1:
                self.agents[num][1] = self.agents[num][1] + 1
            next_state = self.agents[num]
        if self.grid[help_next_sate[0]][help_next_sate[1]] == 1:
            reward = -3000
            if self.isDone(self.grid): done = True
            return next_state, reward, done
        if self.grid[self.agents[num][0]][self.agents[num][1]] == 0:
            reward = -33
            if self.isDone(self.grid): done = True
            return next_state, reward, done
        if self.grid[self.agents[num][0]][self.agents[num][1]] == 2:
            self.grid[self.agents[num][0]][self.agents[num][1]] = 0
            reward = 30
            if self.isDone(self.grid): done = True
            return next_state, reward, done

    def get_global_obs(self):
        obs = np.zeros((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.grid[i, j] == 0:
                    obs[i, j, 0] = 1
                    obs[i, j, 1] = 1
                    obs[i, j, 2] = 1
                if self.grid[i, j] == 2:
                    obs[i, j, 0] = 0
                    obs[i, j, 1] = 1
                    obs[i, j, 2] = 0
        for i in range(self.N_agent):
            obs[self.agents[i][0], self.agents[i][1], 0] = 1
            obs[self.agents[i][0], self.agents[i][1], 1] = 0
            obs[self.agents[i][0], self.agents[i][1], 2] = 0
        return obs

    def reset(self):
        self.grid = self.generate_maze(self.seed)
        self.agents = []
        self.agents.append([1, 1])
        self.agents.append([1, 1])

    def render(self):
        obs = self.get_global_obs()
        enlarge = 100
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
                    cv2.circle(new_obs, (i * enlarge + 50, j * enlarge + 50), 30,
                               (0, 234, 100), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(10)

    def isDone(self, grid):
        for row in grid:
            if 2 in row:
                return False
        return True

    def numOf2(self):
        num = 0
        for row in self.grid:
            for cislo in row:
                if cislo == 2:
                    num += 1
        return num
