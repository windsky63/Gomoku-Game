import numpy as np
from copy import deepcopy
from collections import deque


class GomokuGame:
    def __init__(self, size=10):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.last_move = (None, (None, None))
        self.current_player = 1  # 玩家1为先手，2为后手
        self.game_over = False
        self.winner = None

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for key, value in self.__dict__.items():
            setattr(result, key, deepcopy(value, memo))
        return result

    def set(self, **kwargs):
        size = kwargs.get('size', 10)
        self.size = size
        self.board = np.array(kwargs.get('board', np.zeros((size, size), dtype=int)))
        self.current_player = kwargs.get('current_player', 1)
        self.game_over = kwargs.get('game_over', False)
        self.winner = kwargs.get('winner', None)

    def copy(self):
        return deepcopy(self)

    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        return self.get_state()

    def get_state(self):
        return self.board.copy(), self.current_player, self.game_over, self.winner

    def get_valid_points(self):
        return np.where(self.board == 0, 1, 0)

    def step(self, action):
        if self.game_over:
            return self.get_state()

        if not self.check_point_empty(action):
            return self.get_state()

        # 有效行动
        x, y = action
        self.board[x, y] = self.current_player
        self.last_move = (self.current_player, action)

        # 检查是否胜利
        if self.check_win(x, y):
            self.game_over = True
            self.winner = self.current_player
        # 没有胜利则检查是否还有空位置（平局）
        elif np.all(self.board != 0):
            self.game_over = True

        # 没有结束则切换玩家
        if not self.game_over:
            self.current_player = 3 - self.current_player

        return self.get_state()

    def check_win(self, x, y):
        max_count = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横 竖 斜 反斜

        for i, j in directions:
            count, _ = self.check_line(x, y, i, j)
            if count > max_count:
                max_count = count
        if max_count >= 5:
            return True
        else:
            return False

    def check_line(self, x, y, dx, dy):
        """检查在一条线上有多少个相连棋子"""
        player = self.board[x, y]
        positions = [(x, y)]
        count = 1
        # 正向检查
        nx, ny = x + dx, y + dy
        while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == player:
            count += 1
            positions.append((nx, ny))
            nx += dx
            ny += dy
        # 反向检查
        nx, ny = x - dx, y - dy
        while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == player:
            count += 1
            positions.append((nx, ny))
            nx -= dx
            ny -= dy
        return count, positions

    def check_boarder(self, point):
        """检查是否在边界内"""
        x, y = point
        return (0 <= x <= self.size - 1) & (0 <= y <= self.size - 1)

    def check_point_empty(self, point):
        """检查当前点是否为空"""
        if not self.check_boarder(point):
            return False
        x, y = point
        return self.board[x][y] == 0


def get_nearby_points(board, n=4):
    """
    获取棋盘上已有棋子位置旁边（最多距离n个空格）的所有空位，优先考虑靠近已有棋子的位置

    参数:
        board: NumPy数组表示的棋盘，0表示空位，1表示棋子
        n: 距离棋子的最大空格数（默认为4，因为五子棋最长需要4格就能形成五连）

    返回:
        包含所有符合条件的空位坐标的列表，按优先级排序（离已有棋子越近优先级越高），格式为[(x, y), ...]
    """
    # 创建一个与棋盘大小相同的数组，存储每个位置到最近棋子的距离
    distance_matrix = np.full_like(board, 1000, dtype=int)

    # 找到所有棋子的位置，并初始化距离为0
    stone_positions = np.where(board != 0)
    for x, y in zip(stone_positions[0], stone_positions[1]):
        distance_matrix[x, y] = 0

    # 使用广度优先搜索计算每个空位到最近棋子的距离
    queue = deque()

    # 将所有棋子位置加入队列
    for x, y in zip(stone_positions[0], stone_positions[1]):
        queue.append((x, y))

    # 定义8个方向的偏移量
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # 执行广度优先搜索
    while queue:
        x, y = queue.popleft()
        current_distance = distance_matrix[x, y]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.shape[0] and 0 <= ny < board.shape[1]:
                if board[nx, ny] == 0 and distance_matrix[nx, ny] > current_distance + 1:
                    distance_matrix[nx, ny] = current_distance + 1
                    queue.append((nx, ny))

    # 获取所有空位且距离小于等于n的位置
    valid_points = np.argwhere((board == 0) & (distance_matrix <= n))

    if len(valid_points) > 0:
        return valid_points
    else:
        # 计算棋盘中心
        center = np.array(board.shape) // 2
        return np.array([[center[0], center[1]]])


if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]
    print(get_nearby_points(np.array(board), n=1))
    pass
