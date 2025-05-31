import random
import numpy as np
from MCTS.GomokuEnv import GomokuGame


class RuleStrategy:
    """
    基于规则的模型
    (1)当我方有4个棋子相连且一头为空时,落到其中一头
    (2)当对手有4个棋子相连且一头为空时,堵住连珠
    (3)当我方有3个棋子相连且两头为空时,落到其中一头.优先落到连续空位置大于1的一头(例如OOXXXO,X表示棋子,O表示空位置,应该落到左侧),如果都是1个空位置则任选一头
    (4)当对手有3个棋子相连且两头为空,落到其中一头.其中至少有一头的空位置大于1,否则没必要堵住(例如OXXXO)
    (5)不符合上述所有情况,则随机选择位置（靠近棋盘中心）
    """

    def __init__(self, game_env: GomokuGame):
        self.game_env: GomokuGame = game_env
        # 当前行动的玩家
        self.player = game_env.current_player
        self.rival = 3 - game_env.current_player

    def get_empty_positions(self):
        """获取所有空位置"""
        return np.argwhere(self.game_env.board == 0)

    def check_line_for_pattern(self, x, y, dx, dy):
        """检查指定方向上的连线模式"""
        count, positions = self.game_env.check_line(x, y, dx, dy)

        # 检查两端空位
        left_empty = 0
        left_positions = []
        right_empty = 0
        right_positions = []

        # 左端检查
        l1 = (positions[0][0] - dx, positions[0][1] - dy)
        if self.game_env.check_boarder(l1) and self.game_env.check_point_empty(l1):
            left_empty += 1
            left_positions.append(l1)
            # 继续向左检查连续空位
            temp_x, temp_y = positions[0][0] - dx, positions[0][1] - dy
            while self.game_env.check_boarder((temp_x, temp_y)) and self.game_env.check_point_empty((temp_x, temp_y)):
                left_empty += 1
                left_positions.append((temp_x, temp_y))
                temp_x -= dx
                temp_y -= dy

        # 右端检查
        r1 = (positions[-1][0] + dx, positions[-1][1] + dy)
        if self.game_env.check_boarder(r1) and self.game_env.check_point_empty(r1):
            right_empty += 1
            right_positions.append(r1)
            # 继续向右检查连续空位
            temp_x, temp_y = positions[-1][0] + dx, positions[-1][1] + dy
            while self.game_env.check_boarder((temp_x, temp_y)) and self.game_env.check_point_empty((temp_x, temp_y)):
                right_empty += 1
                right_positions.append((temp_x, temp_y))
                temp_x += dx
                temp_y += dy

        return count, left_empty, right_empty, positions, left_positions, right_positions

    def find_pattern(self, player, n):
        """查找符合n连珠模式的所有位置"""
        patterns = []
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、斜、反斜

        for x in range(self.game_env.size):
            for y in range(self.game_env.size):
                if self.game_env.board[x, y] != player:
                    continue

                for dx, dy in directions:
                    res = self.check_line_for_pattern(x, y, dx, dy)

                    if res[0] == n:
                        patterns.append(res)

        return patterns

    def rule1(self, n=4):
        """规则1: 当我方有4个棋子相连且一头为空时,落到其中一头"""
        if self.player is None:
            return None

        patterns = self.find_pattern(self.player, n)

        for count, left_empty, right_empty, positions, left_positions, right_positions in patterns:
            if left_empty > 0 or right_empty > 0:
                # 优先选择空位更多的一端
                if left_empty > right_empty:
                    return left_positions[0]
                else:
                    return right_positions[0]

        return None

    def rule2(self, n=4):
        """规则2: 当对手有4个棋子相连且一头为空时,堵住连珠"""
        if self.player is None:
            return None

        patterns = self.find_pattern(self.rival, n)

        for count, left_empty, right_empty, positions, left_positions, right_positions in patterns:
            if left_empty > 0 or right_empty > 0:
                # 优先选择空位更多的一端
                if left_empty > right_empty:
                    return left_positions[0]
                else:
                    return right_positions[0]

        return None

    def rule3(self, n=3):
        """规则3: 当我方有3个棋子相连且两头为空时,落到其中一头.优先落到连续空位置更多的一头"""
        if self.player is None:
            return None

        patterns = self.find_pattern(self.player, n)

        for count, left_empty, right_empty, positions, left_positions, right_positions in patterns:
            if left_empty > 0 or right_empty > 0:
                # 优先选择空位更多的一端
                if left_empty > right_empty:
                    return left_positions[0]
                elif right_empty > left_empty:
                    return right_positions[0]
                else:
                    return random.choice([left_positions[0], right_positions[0]])

        return None

    def rule4(self, n=3):
        """规则4: 当对手有3个棋子相连且两头为空,落到其中一头.其中至少有一头的空位置大于0"""
        if self.player is None:
            return None

        patterns = self.find_pattern(self.rival, n)

        for count, left_empty, right_empty, positions, left_positions, right_positions in patterns:
            # 检查是否已经堵住至少一端
            if left_empty > 0 and right_empty > 0:
                # 优先选择空位更多的一端
                if left_empty > right_empty:
                    return left_positions[0]
                else:
                    return right_positions[0]

        return None

    def rule5(self):
        """规则5: 随机选择位置（偏向棋盘中心）"""
        empty_positions = self.get_empty_positions()
        if len(empty_positions) == 0:
            return None

        # 计算所有空位到中心的距离
        center_x, center_y = self.game_env.size // 2, self.game_env.size // 2
        positions_with_distance = [{'position': (x, y), 'distance': abs(x - center_x) + abs(y - center_y)} for x, y in empty_positions]

        # 按距离中心从近到远排序
        positions_sorted = sorted(positions_with_distance, key=lambda p: p['distance'])

        # 创建一个权重列表，距离越近权重越高
        # 这里使用距离的倒数作为权重，确保中心位置有更高概率被选中
        weights = [1 / (p['distance'] + 1) for p in positions_sorted]  # +1避免除以0

        # 归一化权重
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # 根据权重随机选择一个位置
        selected = random.choices(positions_sorted, weights=normalized_weights, k=1)[0]

        return selected['position']

    def rule6(self):
        """规则6: 完全随机选择位置"""
        empty_positions = self.get_empty_positions()
        if len(empty_positions) == 0:
            return None
        return tuple(empty_positions[random.randint(0, len(empty_positions) - 1)])

    def model(self):
        """主决策函数"""
        rule_chain = [self.rule1, self.rule2, self.rule3, self.rule4, self.rule5]
        for rule in rule_chain:
            res = rule()
            if res is not None:
                # 检查位置是否有效
                x, y = res
                if self.game_env.check_boarder((x, y)) and self.game_env.check_point_empty((x, y)):
                    return res

