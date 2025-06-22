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
- **并行计算优化**: 实现了多线程/多进程的MCTS计算（可选）

## 项目结构

```
gomoku-ai/
├── backend/                # Django后端项目
│   ├── gomoku/             # 主应用
│   │   ├── ai/             # AI算法实现
│   │   │   └── mcts.py     # MCTS算法核心实现
│   │   ├── api/            # API视图
│   │   ├── models.py       # 数据库模型
│   │   ├── serializers.py  # 序列化器
│   │   └── ...             # 其他应用文件
│   ├── config/             # 项目配置
│   └── manage.py           # Django管理命令
├── frontend/               # Vue前端项目
│   ├── src/
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # Vue组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # Pinia状态管理
│   │   ├── views/          # 页面视图
│   │   ├── App.vue         # 根组件
│   │   └── main.ts         # 入口文件
│   ├── index.html          # HTML模板
│   └── vite.config.ts      # Vite配置
├── docs/                   # 项目文档
├── requirements.txt        # Python依赖
├── package.json            # npm依赖
└── README.md               # 本文件
```

## 功能特点

1. **AI对战模式**
   - 基于MCTS算法的智能AI对手
   - 可调节AI难度级别（通过调整MCTS参数）
   - 支持悔棋功能

2. **用户界面**
   - 响应式设计，适配不同屏幕尺寸
   - 美观的棋盘和棋子设计
   - 游戏状态显示（当前回合、胜负判定等）

3. **游戏功能**
   - 标准的五子棋规则
   - 胜负判定系统
   - 游戏记录保存（可选）

4. **开发特性**
   - 前后端分离架构
   - 完整的API文档
   - 单元测试覆盖核心算法

## 安装与运行

### 前端安装
```bash
cd frontend
npm install
npm run dev  # 开发模式
npm run build  # 生产构建
```

### 后端安装
```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
cd backend
python manage.py migrate

# 运行开发服务器
python manage.py runserver
```

## 算法说明

### MCTS实现

1. **选择(Selection)**: 使用UCT算法选择最有潜力的节点
2. **扩展(Expansion)**: 在当前节点下扩展新的子节点
3. **模拟(Simulation)**: 从新节点开始进行随机模拟，直到游戏结束
4. **回溯(Backpropagation)**: 将模拟结果回溯到根节点，更新统计信息

### 优化策略

- **并行计算**: 使用多线程/多进程加速MCTS搜索
- **启发式评估**: 在模拟阶段使用简单的启发式函数评估棋局
- **透明表(Transposition Table)**: 缓存已评估的棋局状态
- **迭代加深**: 逐步增加搜索深度

## 扩展建议

1. **算法优化**
   - 实现更高效的启发式评估函数
   - 添加神经网络指导的MCTS（AlphaZero风格）
   - 优化并行计算策略

2. **功能增强**
   - 添加网络对战功能
   - 实现棋谱记录和回放
   - 添加AI训练模式

3. **用户体验**
   - 添加音效和动画效果
   - 实现移动端适配优化
   - 添加游戏统计和分析功能

## 贡献指南

欢迎对本项目进行贡献！请遵循以下步骤：

1. Fork本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 许可证

本项目采用[MIT许可证](LICENSE) - 详情请参见LICENSE文件。

---

希望这个README能够帮助您了解这个五子棋人机对战项目的设计和实现。如需更详细的信息，可以查看项目中的具体代码和文档。
