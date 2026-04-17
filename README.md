# Agent-Customer-Service

基于 LangGraph 的企业级 AI 客服系统，支持多意图路由、RAG 问答、NL2SQL 订单处理、闲聊和人工转接。

## 技术栈

- **框架**：LangGraph (LangChain)
- **语言模型**：DeepSeek（路由）、Qwen（聊天/RAG）、MiniMax（NL2SQL）
- **向量库**：Chroma | **数据库**：PostgreSQL + MySQL | **API**：FastAPI

## 项目结构

```
├── main.py                    # FastAPI 入口
├── graph/
│   ├── customer_graph.py      # LangGraph 工作流
│   ├── state.py               # 状态定义
│   └── nodes/
│       ├── router.py          # 意图路由（LLM 分类）
│       ├── faq_agent.py      # FAQ 节点（RAG）
│       ├── order_agent.py    # 订单节点（NL2SQL）
│       ├── chat_node.py      # 闲聊节点
│       └── human_node.py     # 人工转接节点（interrupt）
├── rag/                       # RAG 服务
├── service/
│   ├── chat_service.py       # 闲聊服务
│   ├── order_service.py      # NL2SQL 服务
│   └── human_service.py      # 人工客服 WebSocket
└── prompts/                   # 提示词模板
```

## 开发进度

### ✅ 已完成

| 需求 | 描述 | 实现 |
|------|------|------|
| REQ-001 | 意图识别与路由 | `router.py` - DeepSeek 结构化输出 |
| REQ-002 | FAQ 知识库问答 | `rag_service.py` - Qwen + Chroma RAG |
| REQ-003 | 状态持久化 | `customer_graph.py` - PostgresSaver |
| REQ-004 | 人工介入 | `human_node.py` - interrupt() + WebSocket |
| REQ-005 | NL2SQL 订单查询 | `order_service.py` - SQLDatabaseToolkit |
| REQ-007 | 对话摘要压缩 | `chat_node.py` - 超过阈值时压缩历史 |

### 🔧 下一步优化点

| 需求 | 描述 | 说明 |
|------|------|------|
| REQ-006 | 流式输出 | 支持打字机效果（可选） |
| REQ-008 | Supervisor Agent | 多 Agent 协作，支持上下文关联与回答质量评估 |
| REQ-009 | 情感分析 | 负面情绪自动转人工 |
| REQ-010 | LangSmith 追踪 | 配置环境变量即可 |

## 启动

```bash
# 1. 配置 config/config.yaml（API keys、数据库连接）

# 2. 启动依赖服务
# - PostgreSQL（会话持久化）
# - ChromaDB（RAG 向量库）
# - MySQL（业务数据）

# 3. 启动服务
python main.py                      # 主服务（端口 8001）
python service/human_service.py     # 人工客服 WebSocket（端口 8000）
```

## API

### POST /api/chat

```json
// 请求
{"user_id": "user123", "message": "查询我的最新订单"}

// 响应
{"mode": "ai", "history": [...], "reply": "您的订单已发货"}
```

- `mode`: `ai` - AI 回复，`human` - 等待人工客服

## 工作流程

```
用户输入 → 意图路由（DeepSeek）
              ↓
    ┌─────────┼─────────┬─────────┐
    ↓         ↓         ↓         ↓
  FAQ     Order      Chat     Human
 (RAG)   (NL2SQL)   (闲聊)   (转人工)
    └─────────┴─────────┴─────────┘
                    ↓
                最终回复
```

## 注意事项

- `config/config.yaml` 包含敏感信息，已 gitignore
- PostgreSQL、ChromaDB、MySQL 服务需提前启动
