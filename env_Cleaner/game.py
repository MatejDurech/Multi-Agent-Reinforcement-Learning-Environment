import random
from env import Env

from heapq import heappop, heappush
import copy
import time
from bfs import BFS
from marl import MARL

if __name__ == '__main__':
    env = Env(2, 5)  # 5,6,2,9,10,16
    env.render()
    bfs_team = BFS()
    bfs_team.bfs_team_run(env)
    env.reset()
    marl_team = MARL()
    q1, q2 = marl_team.training(env)
    env.reset()
    marl_team.run(env, q1, q2)


