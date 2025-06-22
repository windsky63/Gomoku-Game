# 五子棋人机对战项目

## 项目简介

这是一个基于蒙特卡洛树搜索(MCTS)算法实现的五子棋人机对战系统，结合了Vue.js前端框架和Django后端框架，提供了一个完整的五子棋游戏体验，用户可以与AI进行对战。

## 技术栈

### 前端 (Vue.js)
- **Vue 3**: 用于构建用户界面的渐进式JavaScript框架
- **Vue Router**: 实现前端路由管理
- **Pinia**: 状态管理库，替代Vuex
- **Element Plus**: 基于Vue 3的UI组件库，用于快速构建美观的界面
- **Vite**: 前端构建工具，提供快速的开发体验
- **TypeScript**: 为JavaScript添加类型系统，提高代码可维护性

### 后端 (Django)
- **Django 4.x**: 高级Python Web框架，用于构建后端API
- **Django REST Framework**: 构建RESTful API的强大工具
- **Django Channels**: 用于实现WebSocket通信（可选，用于实时对战功能）
- **SQLite/PostgreSQL**: 数据库选择（开发使用SQLite，生产环境建议PostgreSQL）
- **Celery**: 异步任务队列（可选，用于优化MCTS计算）
- **Redis**: 作为Celery的broker和结果后端（可选）

### 核心算法
- **蒙特卡洛树搜索(MCTS)**: 用于AI决策的核心算法
- **启发式评估函数**: 结合五子棋规则的评估函数，优化MCTS性能

## 功能特点

1. **AI对战模式**
   - 基于MCTS算法的智能AI对手
   - 可调节AI难度级别（通过调整MCTS参数）

2. **用户界面**
   - 美观的棋盘和棋子设计
   - 游戏状态显示（当前回合、胜负判定等）

3. **游戏功能**
   - 标准的五子棋规则
   - 胜负判定系统

## 算法说明

### MCTS实现

1. **选择(Selection)**: 使用UCT算法选择最有潜力的节点
2. **扩展(Expansion)**: 在当前节点下扩展新的子节点
3. **模拟(Simulation)**: 从新节点开始进行随机模拟，直到游戏结束
4. **回溯(Backpropagation)**: 将模拟结果回溯到根节点，更新统计信息

### 优化策略

- **启发式评估**: 在模拟阶段使用简单的启发式函数评估棋局
- **透明表(Transposition Table)**: 缓存已评估的棋局状态
- **迭代加深**: 逐步增加搜索深度

