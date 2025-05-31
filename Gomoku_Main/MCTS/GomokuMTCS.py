import numpy as np
from MCTS.GomokuEnv import GomokuGame, get_nearby_points
from MCTS.GomokuRule import RuleStrategy
import random
from math import sqrt, log


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state: GomokuGame = state  # 状态
        self.parent = parent  # 父节点
        if move is None:
            self.move = (state.current_player, None)
        else:
            self.move = move  # 到达当前节点采取的行动，在五子棋环境中需要为(player, action)，即记录玩家执行的动作
        self.children = []  # 子节点列表
        self.wins = 0
        self.if_winner = None  # 表示当前节点经过模拟后可能的胜利者，None为当前节点没有胜利者
        self.visits = 0
        self.untried_actions = None
        self.nearby_actions = None

    def get_untried_actions(self):
        """
        获取所有没有棋子的位置
        """
        valid_moves = np.argwhere(self.state.get_valid_points() == 1)
        return [tuple(move) for move in valid_moves]

    def get_nearby_actions(self):
        """
        获取已有棋子的位置邻近的没有棋子的位置
        """
        valid_moves = get_nearby_points(self.state.board, n=2)
        return [tuple(move) for move in valid_moves]

    def select_child(self, ucb_c=np.log(2)):
        selected_child = None
        best_value = 0.0
        for child in self.children:
            v = child.wins
            n = child.visits
            if n == 0:
                uct_value = 99999
            else:
                uct_value = (v / n) + (ucb_c * sqrt(2 * log(self.visits) / n))
            if uct_value > best_value:
                best_value = uct_value
                selected_child = child
        return selected_child

    def expand(self):
        if self.untried_actions is None:
            self.untried_actions = self.get_untried_actions()
        for ua in self.untried_actions:
            new_state = self.state.copy()
            new_state.step(ua)
            new_node = MCTSNode(new_state, parent=self, move=(self.state.current_player, ua))
            self.children.append(new_node)
        self.untried_actions = None
        return new_node

    def expand_nearby(self):
        """
        仅扩展邻近节点
        """
        if self.nearby_actions is None:
            self.nearby_actions = self.get_nearby_actions()
        for na in self.nearby_actions:
            new_state = self.state.copy()
            new_state.step(na)
            new_node = MCTSNode(new_state, parent=self, move=(self.state.current_player, na))
            self.children.append(new_node)
        self.nearby_actions = None
        return new_node

    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0


class MCTSTree:
    def __init__(self, root_node: MCTSNode):
        self.SIMULATION_DEPTH = 1000
        self.SIMULATION_TIMES = 100
        self.ONLY_NEARBY: bool = False
        self.root_node: MCTSNode = root_node

    def selection(self, node: MCTSNode):
        """
        根据UCB选择最佳的节点,直到叶子节点.如果没有子节点则返回自己
        """
        # 如果没有子节点则跳过
        if len(node.children) == 0:
            return node
        # 循环找到叶子节点
        while True:
            child_node = node.select_child()
            if child_node is None:
                break
            node = child_node
        return node

    def expansion(self, node: MCTSNode):
        """
        如果选择的节点不是叶子节点或当前胜负已分则不需要扩展
        遍历棋盘所有空的位置设置为其子节点
        """
        if len(node.children) > 0:
            return node
        if node.if_winner:
            return node
        # 节点进行扩展
        if self.ONLY_NEARBY:
            node.expand_nearby()
        else:
            node.expand()
        return random.choice(node.children)

    def simulation(self, node: MCTSNode):
        """
        从扩展的子节点做模拟,直到游戏结束或达到预设的深度
        """
        # 查看当前节点是否获胜
        if node.if_winner:
            return node.state.winner
        g = node.state.copy()
        i = 0
        winner = None

        while True:
            i += 1
            action = RuleStrategy(g).model()
            _, _, _, res_winner = g.step(action)
            # 判断退出条件
            if res_winner is not None:
                winner = res_winner
                break
            if i >= self.SIMULATION_DEPTH:
                break
        if winner is None:
            pass
        else:
            print()
            node.if_winner = winner
        return winner

    def backpropagation(self, node: MCTSNode):
        """
        将模拟结果反向传播给沿途阶段,包括访问次数和胜利次数
        将沿途节点访问次数加1
        如果胜利将沿途节点胜利方胜利次数加1,平局则加0.1
        """
        cur_node = node
        winner = cur_node.if_winner
        while cur_node is not None:
            cur_node.visits += 1
            if winner is not None:
                if winner != 0 and winner == self.root_node.state.current_player:
                    cur_node.wins += 1
            else:
                cur_node.wins += 0.1
            cur_node = cur_node.parent

    def pruning(self):
        # 根据规则AI判断下一步动作
        state = self.root_node.state
        rule_strategy = RuleStrategy(state)
        rule_chain = [rule_strategy.rule1, rule_strategy.rule2, rule_strategy.rule3, rule_strategy.rule4]
        # 匹配到规则, 直接按新的下法剪枝
        for rule in rule_chain:
            res = rule()
            if res is not None:
                state.step(res)
                new_node = MCTSNode(state, parent=self.root_node, move=(3 - state.current_player, res))
                self.root_node.children.append(new_node)
                # 设置新节点为根节点
                self.root_node = new_node
                print(f"触发规则,直接使用RuleStrategy模型,落点为{res}")
                return new_node.move

    def model(self, print_simulation_result=False):
        """
        产生一个树,叶子节点的棋盘设置为cur_board.按以下步骤进行迭代
        (1)选择
        第一轮迭代,由于当前树只有1个节点,没有子节点,因此跳过
        后续迭代中,找到所有子节点,计算所有子节点的UCB值,选择UCB值最大的节点
        (2)扩展
        如果选择的节点是非叶子节点或者此节点的胜负关系已分,则不需要扩展
        将剩余所有的下法作为子节点追加到根节点上,并任取其中一个节点作为当前节点
        (3)仿真
        如果选择的节点胜负已分,则不需要仿真
        从当前节点往后仿真对局,可叠加rule_strategy,直到游戏结束或深度超过预设值
        (4)回溯
        根据胜负关系,更新当前节点到根节点的沿途所有节点的win_num和visit_num
        """
        # 匹配规则剪枝
        # res = self.pruning()
        # if res is not None:
        #     return res
        # 未匹配到规则, 使用MCTS算法
        for i in range(self.SIMULATION_TIMES):
            print(f"第{i}次模拟")
            next_node = self.selection(self.root_node)
            next_node = self.expansion(next_node)
            self.simulation(next_node)
            self.backpropagation(next_node)

        if print_simulation_result:
            for n in self.root_node.children:
                print(f'访问次数{n.visits} 胜利次数{n.wins} 节点对应行动{n.move}')

        # 选择忽略探索的最优子节点
        new_node = self.root_node.select_child(ucb_c=0)
        # 设置最优子节点为根节点
        self.root_node = new_node
        return new_node.move


if __name__ == "__main__":
    # board = [[2, 0, 0, 0, 0, 0],
    #          [1, 2, 0, 0, 0, 0],
    #          [1, 0, 2, 0, 0, 0],
    #          [0, 1, 0, 2, 0, 0],
    #          [0, 0, 1, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0]]
    # board = [[0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0],
    #          [0, 0, 2, 2, 2, 2],
    #          [0, 0, 0, 0, 0, 1],
    #          [0, 0, 0, 0, 1, 1],
    #          [0, 0, 1, 0, 0, 0]]
    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0],
             [0, 2, 2, 2, 0, 2],
             [0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 1],
             [0, 1, 0, 0, 0, 0]]
    # board = [[0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 1, 0, 0],
    #          [0, 2, 0, 2, 2, 2],
    #          [0, 0, 0, 0, 0, 1],
    #          [0, 0, 0, 0, 1, 1],
    #          [0, 0, 0, 0, 0, 0]]
    game = GomokuGame()
    game.set(board=board, size=6)
    node = MCTSNode(game, move=(2, (2, 1)))
    s = MCTSTree(node)
    print(s.model(print_simulation_result=True))

