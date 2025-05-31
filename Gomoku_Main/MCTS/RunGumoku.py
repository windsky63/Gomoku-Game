from MCTS.GomokuEnv import GomokuGame
from MCTS.GomokuMTCS import MCTSNode, MCTSTree


def human_vs_ai(simulation_times=100, simulation_depth=1000):
    """
    人机对战函数

    参数:
        board_size: 棋盘大小 (默认6x6)
        simulation_times: MCTS模拟次数
        simulation_depth: 模拟深度
    """
    # 初始化游戏
    game = GomokuGame()
    current_player = 1  # 假设人类玩家使用1表示，AI使用2表示

    print("欢迎来到五子棋人机对战游戏!")
    print("人类玩家使用1表示，AI玩家使用2表示")
    print("输入坐标格式为: 行,列 (例如: 3,4 表示第4行第5列)")

    # 显示初始棋盘
    print("\n当前棋盘:")
    print(game.board)

    while True:
        if game.winner is not None:
            print("\n游戏结束! 玩家{}获胜!".format(game.winner))
            break

        if current_player == 1:  # 人类玩家回合
            # 获取人类玩家输入
            while True:
                try:
                    move_input = input("\n人类玩家({})的回合，请输入你的落子坐标(例如: 3,4): ".format(current_player))
                    row, col = map(int, move_input.split(','))

                    # 验证输入是否有效
                    if not game.check_boarder((row, col)):
                        print("坐标超出范围，请重新输入!")
                        continue

                    if game.board[row][col] != 0:
                        print("该位置已有棋子，请重新输入!")
                        continue

                    break
                except ValueError:
                    print("输入格式错误，请按格式'行,列'输入，例如: 3,4")

            # 执行人类玩家的移动
            human_action = (row, col)
            game.step(human_action)
            print("\n人类玩家落子于: ({}, {})".format(row, col))

        else:  # AI玩家回合
            print("\nAI玩家({})正在思考...".format(current_player))

            # 创建MCTS树
            root_node = MCTSNode(game.copy(), move=(1, human_action))
            mcts = MCTSTree(root_node)
            mcts.SIMULATION_TIMES = simulation_times
            mcts.SIMULATION_DEPTH = simulation_depth

            # 让MCTS选择最佳移动
            ai_move = mcts.model(print_simulation_result=False)[1]  # 获取移动坐标

            # 执行AI的移动
            game.step(ai_move)
            print("AI玩家落子于: ({}, {})".format(ai_move[0], ai_move[1]))

        # 显示当前棋盘状态
        print("\n当前棋盘:")
        print(game.board)

        # 切换玩家
        current_player = 3 - current_player  # 在1和2之间切换


# 运行人机对战
if __name__ == "__main__":
    human_vs_ai(simulation_times=50, simulation_depth=1000)

