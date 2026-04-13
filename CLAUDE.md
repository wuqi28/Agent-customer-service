# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指导。

## 项目概述

基于 LangGraph 构建的企业级 AI 客服系统，支持多意图路由、RAG 问答、订单处理、闲聊和人工转接。

## 运行应用

```bash
python main.py
```

启动 FastAPI 服务于 `127.0.0.1:8001`。需要 PostgreSQL 和 ChromaDB 服务已运行。

## 架构

### LangGraph 工作流

核心代理是定义在 `graph/customer_graph.py` 中的 `StateGraph`，流程：

```
START → router → [faq | order | chat | human] → END
```

- **router** (`graph/nodes/router.py`)：使用 DeepSeek 进行意图分类（结构化输出），分为 `faq`、`order`、`chat`、`complaint`、`escalation`。置信度 < 0.7 触发转人工。
- **faq** (`graph/nodes/faq_agent.py`)：基于 RAG 的 FAQ 检索，使用 Qwen + Chroma 向量库。
- **order** (`graph/nodes/order_agent.py`)：订单相关查询处理。
- **chat** (`graph/nodes/chat_node.py`)：使用 Qwen 进行通用闲聊。
- **human** (`graph/nodes/human_node.py`)：使用 `interrupt()` 挂起图，等待人工客服通过 WebSocket 介入。

### 状态管理

`graph/state.py` 定义了 `CustomerState` TypedDict：
- `messages`：使用 `operator.add` 注解进行累积
- `intent`、`confidence`：路由输出
- `retrieved_docs`：RAG 检索结果
- `needs_approval`、`requires_human`、`final_response`：流程控制

### 持久化

- **PostgreSQL** (`graph/customer_graph.py`)：LangGraph checkpointer，通过 `PostgresSaver` 实现会话/记忆持久化
- **ChromaDB** (`rag/vector_store.py`)：RAG 文档检索的向量库

### API

`POST /api/chat` 接收 `{user_id, message}`，返回 `{mode, history, reply}`，其中 mode 为 `ai` 或 `human`。

### 模型工厂

`factory/llm_factory.py` 提供工厂模式：
- `DeepseekChatModelFactory`：意图路由（temperature=0）
- `QwenChatModelFactory`：通用聊天/RAG
- `DashScopeEmbeddingsFactory`：向量库嵌入模型

## 关键文件

| 文件 | 用途 |
|------|------|
| `main.py` | FastAPI 应用 + chat 接口 |
| `graph/customer_graph.py` | LangGraph 工作流定义 |
| `graph/state.py` | 状态 schema |
| `graph/nodes/router.py` | 意图分类节点 |
| `graph/nodes/human_node.py` | 人工转接节点（含 interrupt） |
| `rag/rag_service.py` | RAG 链（检索 + 生成） |
| `factory/llm_factory.py` | LLM 实例化 |
| `config/config.yaml` | 配置文件（含 API keys 等）— 不提交到 git |
