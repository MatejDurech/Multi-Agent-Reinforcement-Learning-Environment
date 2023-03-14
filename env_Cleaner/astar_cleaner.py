import random
from env_Cleaner import EnvCleaner
from heapq import heappop, heappush
import copy


class Path:
    def __init__(self, path):
        self.path = path
        self.last_pos = ""
        self.isFull = False

    def addToPath(self, x, y):
        self.path.append([x, y])

    def getPath(self):
        return self.path

    def setLast_pos(self, pos):
        self.last_pos = pos

    def getLast_pos(self):
        return self.last_pos

    def setIsFull(self, state):
        self.isFull = state

    def len(self):
        return len(self.getPath())


def astar(start_x, start_y, grid):
    paths = list()
    paths.append(Path([[start_x, start_y]]))
    restart = True
    while restart:
        restart = False
        for path in paths:
            help_path = copy.deepcopy(path)
            base_path = copy.deepcopy(path)
            isFirstNeighbour = True
            if grid[base_path.getPath()[len(base_path.getPath()) - 1][0] - 1][
                base_path.getPath()[len(base_path.getPath()) - 1][1]] != 1 and not base_path.isFull:
                # print("tutut1", base_path.getPath())
                if isFirstNeighbour:
                    if path.getLast_pos() != "right":
                        if grid[path.getPath()[len(path.getPath()) - 1][0] - 1][
                            path.getPath()[len(path.getPath()) - 1][1]] == 2:
                            path.setIsFull(True)
                        path.addToPath(path.getPath()[len(path.getPath()) - 1][0] - 1,
                                       path.getPath()[len(path.getPath()) - 1][1])
                        isFirstNeighbour = False
                        path.setLast_pos("left")

                else:
                    if help_path.getLast_pos() != "right":
                        if grid[help_path.getPath()[len(help_path.getPath()) - 1][0] - 1][
                            help_path.getPath()[len(help_path.getPath()) - 1][1]] == 2:
                            help_path.setIsFull(True)
                        help_path.addToPath(help_path.getPath()[len(help_path.getPath()) - 1][0] - 1,
                                            help_path.getPath()[len(help_path.getPath()) - 1][1])
                        help_path.setLast_pos("left")

                        paths.append(help_path)
                        help_path = base_path
            if grid[base_path.getPath()[len(base_path.getPath()) - 1][0] + 1][
                base_path.getPath()[len(base_path.getPath()) - 1][1]] != 1 and not base_path.isFull:
                # print("tutut2", base_path.getPath())
                if isFirstNeighbour:
                    if path.getLast_pos() != "left":
                        if grid[path.getPath()[len(path.getPath()) - 1][0] + 1][
                            path.getPath()[len(path.getPath()) - 1][1]] == 2:
                            path.setIsFull(True)
                        path.addToPath(path.getPath()[len(path.getPath()) - 1][0] + 1,
                                       path.getPath()[len(path.getPath()) - 1][1])
                        isFirstNeighbour = False
                        path.setLast_pos("right")
                else:
                    if help_path.getLast_pos() != "left":
                        if grid[help_path.getPath()[len(help_path.getPath()) - 1][0] + 1][
                            help_path.getPath()[len(help_path.getPath()) - 1][1]] == 2:
                            help_path.setIsFull(True)
                        help_path.addToPath(help_path.getPath()[len(help_path.getPath()) - 1][0] + 1,
                                            help_path.getPath()[len(help_path.getPath()) - 1][1])
                        help_path.setLast_pos("right")
                        paths.append(help_path)
                        help_path = base_path
            if grid[base_path.getPath()[len(base_path.getPath()) - 1][0]][
                base_path.getPath()[len(base_path.getPath()) - 1][1] - 1] != 1 and not base_path.isFull:
                # print("tutut3", base_path.getPath())
                if isFirstNeighbour:
                    if path.getLast_pos() != "down":
                        if grid[path.getPath()[len(path.getPath()) - 1][0]][
                            path.getPath()[len(path.getPath()) - 1][1] - 1] == 2:
                            path.setIsFull(True)
                        path.addToPath(path.getPath()[len(path.getPath()) - 1][0],
                                       path.getPath()[len(path.getPath()) - 1][1] - 1)
                        isFirstNeighbour = False
                        path.setLast_pos("top")
                else:
                    if help_path.getLast_pos() != "down":
                        if grid[help_path.getPath()[len(help_path.getPath()) - 1][0]][
                            help_path.getPath()[len(help_path.getPath()) - 1][1] - 1] == 2:
                            help_path.setIsFull(True)
                        help_path.addToPath(help_path.getPath()[len(help_path.getPath()) - 1][0],
                                            help_path.getPath()[len(help_path.getPath()) - 1][1] - 1)
                        help_path.setLast_pos("top")
                        paths.append(help_path)
                        help_path = base_path
            if grid[base_path.getPath()[len(base_path.getPath()) - 1][0]][
                base_path.getPath()[len(base_path.getPath()) - 1][1] + 1] != 1 and not base_path.isFull:
                # print("tutut4", base_path.getPath())
                if isFirstNeighbour:
                    if path.getLast_pos() != "top":
                        if grid[path.getPath()[len(path.getPath()) - 1][0]][
                            path.getPath()[len(path.getPath()) - 1][1] + 1] == 2:
                            path.setIsFull(True)
                        path.addToPath(path.getPath()[len(path.getPath()) - 1][0],
                                       path.getPath()[len(path.getPath()) - 1][1] + 1)
                        isFirstNeighbour = False
                        path.setLast_pos("down")
                else:

                    if help_path.getLast_pos() != "top":
                        if grid[help_path.getPath()[len(help_path.getPath()) - 1][0]][
                            help_path.getPath()[len(help_path.getPath()) - 1][1] + 1] == 2:
                            help_path.setIsFull(True)
                        help_path.addToPath(help_path.getPath()[len(help_path.getPath()) - 1][0],
                                            help_path.getPath()[len(help_path.getPath()) - 1][1] + 1)
                        help_path.setLast_pos("down")
                        paths.append(help_path)
                        help_path = base_path

            if not isFirstNeighbour:
                restart = True
    defPaths = list()
    for path in paths:
        if grid[path.getPath()[len(path.getPath()) - 1][0]][path.getPath()[len(path.getPath()) - 1][1]] == 2:
            defPaths.append(path)
    defPaths.sort(key=lambda x: len(x.getPath()))
    pathsToReturn = list()
    if len(defPaths) == 0:
        pathsToReturn.append(Path([[start_x, start_y]]))
    elif len(defPaths) == 1:
        pathsToReturn.append(defPaths[0])
    else:
        pathsToReturn.append(defPaths[0])
        pathsToReturn.append(defPaths[1])
    for path in pathsToReturn:
        print(path.getPath())
    return pathsToReturn


def fromPathMakeDirection(path, start_pos_x, start_pos_y):
    if len(path) == 1:
        return random.randint(0, 3)
    else:
        if path[1][0] == start_pos_x - 1 and path[1][1] == start_pos_y: return 0
        if path[1][0] == start_pos_x + 1 and path[1][1] == start_pos_y: return 1
        if path[1][0] == start_pos_x and path[1][1] == start_pos_y - 1: return 2
        if path[1][0] == start_pos_x and path[1][1] == start_pos_y + 1: return 3


if __name__ == '__main__':
    env = EnvCleaner(2, 15, 6) # pouzivat seedy[2,4,6]
    max_iter = 1000
    done = False
    #array = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
    #         [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1],
    #         [1, 0, 1, 0, 1, 1, 1, 2, 2, 2, 1, 2, 1],
    #         [1, 0, 0, 0, 0, 2, 1, 2, 1, 1, 1, 2, 1],
    #         [1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1],
    #         [1, 0, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1],
    #         [1, 0, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1],
    #         [1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    #         [1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    #         [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1],
    #         [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 3, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    while 1:
        env.render()
        if done: break
        agent_a_paths = astar(env.agt_pos_list[0][0], env.agt_pos_list[0][1], env.occupancy)
        agent_b_paths = astar(env.agt_pos_list[1][0], env.agt_pos_list[1][1], env.occupancy)
        agent_a_path = []
        agent_b_path = []
        if agent_a_paths[0].getPath()[-1] == agent_b_paths[0].getPath()[-1] and len(agent_b_paths) > 1:
            agent_a_path = agent_a_paths[0].getPath()
            agent_b_path = agent_b_paths[1].getPath()
        else:
            agent_a_path = agent_a_paths[0].getPath()
            agent_b_path = agent_b_paths[0].getPath()
        print(fromPathMakeDirection(agent_a_path, env.agt_pos_list[0][0], env.agt_pos_list[0][1]))
        print(fromPathMakeDirection(agent_b_path, env.agt_pos_list[1][0], env.agt_pos_list[1][1]))
        action_list = [fromPathMakeDirection(agent_a_path, env.agt_pos_list[0][0], env.agt_pos_list[0][1]), fromPathMakeDirection(agent_b_path, env.agt_pos_list[1][0], env.agt_pos_list[1][1])]
        next_state, reward, done = env.step(action_list)
        print('reward', reward, next_state, done)


