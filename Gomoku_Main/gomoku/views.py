# views.py
from django.http import JsonResponse
from django.views import View
import json
import time
from MCTS.GomokuEnv import GomokuGame
from MCTS.GomokuMTCS import MCTSNode, MCTSTree

# 全局变量存储游戏状态
state = {
    'game': GomokuGame(),
    'simulation_times': 500,  # 不使用邻近扩展节点的10X10的棋盘需要大约500的模拟次数才能做到初具智能
    'simulation_depth': 1000,
    'only_nearby': True,
    'player_first': True,
    'message': '',
}


def get_game_state():
    player, (x, y) = state['game'].last_move
    if x is not None and y is not None:
        x = int(x)
        y = int(y)
    res = {
        'size': state['game'].size,
        'board': state['game'].board.tolist(),
        'current_player': state['game'].current_player,
        'last_move': {'player': player, 'action': {'x': x, 'y': y}},
        'game_over': state['game'].game_over,
        'winner': state['game'].winner,
        'message': state['message'],
    }
    return res


class InitGame(View):
    def get(self, request):
        """初始化游戏状态"""
        state['game'] = GomokuGame()
        state['message'] = "游戏已初始化，人类玩家(1)的回合"
        if not state['player_first']:
            state['game'].current_player = 2
            state['message'] = "游戏已初始化，电脑玩家(2)的回合"
        res = get_game_state()
        return JsonResponse(res)


class PlayerMove(View):
    def post(self, request):
        """处理玩家移动"""
        game = state['game']

        # 检查游戏是否结束
        if game.winner is not None:
            state['message'] = '游戏已结束，玩家 {} 获胜!'.format(game.winner)
            res = get_game_state()
            return JsonResponse(res)

        # 处理人类玩家移动
        if game.current_player == 1:
            try:
                data = json.loads(request.body)
                x, y = data.get('x'), data.get('y')

                if x is None or y is None:
                    raise ValueError("缺少行或列参数")

                x, y = int(x), int(y)

                # 验证输入是否有效
                if not game.check_boarder((x, y)):
                    state['message'] = '坐标超出范围'
                    res = get_game_state()
                    return JsonResponse(res)

                if game.board[x][y] != 0:
                    state['message'] = '该位置已有棋子'
                    res = get_game_state()
                    return JsonResponse(res)

                # 执行人类玩家的移动
                human_action = (x, y)
                game.step(human_action)
                state['message'] = "人类玩家落子于: ({}, {})".format(x, y)

                # 检查游戏是否结束
                if game.winner is not None:
                    state['message'] = "游戏结束! 玩家 {} 获胜!".format(game.winner)
                    res = get_game_state()
                    return JsonResponse(res)

                res = get_game_state()
                return JsonResponse(res)

            except Exception as e:
                print(e)


class AIMove(View):
    def get(self, request):
        """获取AI移动"""
        game = state['game']

        if game.current_player == 2 and game.winner is None:
            try:
                start_time = time.time()
                # 创建MCTS树
                root_node = MCTSNode(game.copy(), move=game.last_move)
                mcts = MCTSTree(root_node)
                mcts.SIMULATION_TIMES = state['simulation_times']
                mcts.SIMULATION_DEPTH = state['simulation_depth']
                mcts.ONLY_NEARBY = state['only_nearby']

                # 让MCTS选择最佳移动
                ai_move = mcts.model(print_simulation_result=False)[1]  # 获取移动坐标

                end_time = time.time()  # 记录结束时间
                think_time = end_time - start_time  # 计算执行时间（秒）

                # 执行AI的移动
                game.step(ai_move)
                state['message'] = f"AI玩家落子于: ({ai_move[0]}, {ai_move[1]})，思考耗时{think_time:.2f}"

                # 检查游戏是否结束
                if game.winner is not None:
                    state['message'] = "游戏结束! 玩家 {} 获胜!".format(game.winner)
                    res = get_game_state()
                    return JsonResponse(res)

                res = get_game_state()
                return JsonResponse(res)

            except Exception as e:
                print(e)


class Settings(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            state['simulation_times'] = data.get('simulation_times', 1000)
            state['simulation_depth'] = data.get('simulation_depth', 500)
            state['only_nearby'] = data.get('only_nearby', True)
            state['player_first'] = data.get('player_first', True)

            res = {'status': True}
            return JsonResponse(res)
        except Exception as e:
            print(e)

