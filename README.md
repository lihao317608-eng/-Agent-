# -Agent-
构建了一个基于多Agent协作的AI内容生成与变现系统，包含趋势分析Agent、内容生成Agent和爆款优化Agent。系统能够自动分析小红书及公众号热点趋势，结合用户痛点生成高质量内容，并通过改写优化提升传播效果。  在实际运行中，该系统可实现日均生成50+篇内容，显著降低内容生产成本，并提升内容曝光率与点击率。整体流程实现了从“热点识别—内容生成—质量优化”的闭环自动化，Token日消耗约100万-200万。
ai_content_agent/
│
├── main.py                # 主流程（调度）
├── agents/
│   ├── trend_agent.py     # 热点分析 Agent
│   ├── content_agent.py   # 内容生成 Agent
│   ├── rewrite_agent.py   # 爆款改写 Agent
│
├── utils/
│   ├── openai_client.py   # API封装
│
├── data/
│   ├── topics.txt         # 输入主题
│
└── output/
    ├── contents.txt       # 生成结果
