from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage
from graph.customer_graph import build_graph  # 导入你的图构建函数
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
graph = build_graph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，开发阶段最方便
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法 (POST, GET 等)
    allow_headers=["*"],  # 允许所有请求头
)


class ChatRequest(BaseModel):
    user_id: str
    message: str


def format_messages(messages: list) -> List[Dict]:
    """将 LangChain 的消息对象转为前端易读的字典格式"""
    formatted = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            # 处理人工客服的特殊前缀或普通 AI 回复
            content = msg.content
            role = "agent" if "[人工客服]" in content else "ai"
            formatted.append({"role": role, "content": content})
        elif isinstance(msg, str):  # 兼容字符串格式
            formatted.append({"role": "unknown", "content": msg})
    return formatted


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": req.user_id}}

    # 1. 检查当前是否已经在人工模式中
    state = graph.get_state(config)
    is_suspended = state.tasks and any(task.interrupts for task in state.tasks)

    if is_suspended:
        # 人工模式下：不跑 AI，直接把消息存进数据库，并拉取历史返回
        graph.update_state(config, {"messages": [HumanMessage(content=req.message)]})
        # 重新获取更新后的状态
        new_state = graph.get_state(config)
        return {
            "mode": "human",
            "history": format_messages(new_state.values.get("messages", [])),
            "reply": "人工客服正在接入，请稍候..."
        }

    # 2. AI 模式：运行大模型
    # 注意：这里我们传入 user_input，图会自动流转
    res = graph.invoke({"user_input": req.message, "user_id": req.user_id}, config=config)

    # 3. 运行后检查：是否刚刚触发了中断（踩了刹车）？
    post_run_state = graph.get_state(config)
    now_suspended = post_run_state.tasks and any(task.interrupts for task in post_run_state.tasks)

    history = format_messages(post_run_state.values.get("messages", []))

    if now_suspended:
        # 触发了转人工！
        return {
            "mode": "human",
            "history": history,
            "reply": "AI已为您呼叫人工客服，正在转接中..."
        }

    # 正常 AI 回复
    return {
        "mode": "ai",
        "history": history,
        "reply": res.get("final_response", "AI 回复完毕")
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
