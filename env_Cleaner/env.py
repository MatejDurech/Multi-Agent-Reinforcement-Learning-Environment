import numpy as np
import maze
import random
import cv2


class Env(object):
    def __init__(self, N_agent, seed):
        self.map_size = 7
        self.seed = seed
        self.grid = self.generate_maze(seed)
        self.N_agent = N_agent
        self.agents = []
        self.agents.append([1, 1])
        self.agents.append([1, 1])

    def generate_maze(self, seed):
        maze_obj = maze.Maze(int((self.map_size - 1) / 2), int((self.map_size - 1) / 2), seed)
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


    def reset(self):
        self.grid = self.generate_maze(self.seed)
        self.agents = []
        self.agents.append([1, 1])
        self.agents.append([1, 1])

    def render(self):
        enlarge = 100
        picture = np.ones((self.map_size * enlarge, self.map_size * enlarge, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.grid[i][j] == 1:
                    cv2.rectangle(picture, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge), (0, 0, 0), -1)
                if self.grid[i][j] == 2:
                    cv2.circle(picture, (i * enlarge + 50, j * enlarge + 50), 30, (0, 234, 100), -1)
                if i == self.agents[0][0] and j == self.agents[0][1] or i == self.agents[1][0] and j == self.agents[1][1]:
                    cv2.rectangle(picture, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge), (0, 0, 255), -1)
        cv2.imshow('image', picture)
        cv2.waitKey(10)

    def isDone(self, grid):
        for row in grid:
            if 2 in row:
                return False
        return True

    def numOfCoins(self):
        num = 0
        for row in self.grid:
            for cislo in row:
                if cislo == 2:
                    num += 1
        return num
