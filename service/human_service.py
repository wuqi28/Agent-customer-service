import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command
from fastapi.middleware.cors import CORSMiddleware
from graph.customer_graph import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_graph_instance():
    return build_graph()


@app.websocket("/ws/human_chat/{user_id}")
async def websocket_human_chat(websocket: WebSocket, user_id: str):
    """
    处理实时人工客服对话的 WebSocket 路由
    """
    await websocket.accept()
    print(f"\n[服务端] 🟢 建立连接！正在处理用户: {user_id} 的人工会话")

    # 1. 获取图实例 (不运行图，只作为操作数据库的手柄)
    graph = get_graph_instance()

    # 🎯 核心映射：把 user_id 直接当做 LangGraph 的 thread_id 来读取记忆
    config = {"configurable": {"thread_id": user_id}}

    try:
        while True:
            # 2. 接收前端传来的 JSON 消息
            data = await websocket.receive_json()

            role = data.get("role")  # 消息的角色  用户 or 人工客服
            text = data.get("text", "")  # 文本内容
            action = data.get("action", "chat")  # 是否需要人工接入  chat需要 or end结束对话

            # 处理用户与人工客服的对话，写入agent记忆
            if action == "chat":
                if role == "user":
                    # 用户发的消息，悄悄写进 PostgreSQL 记忆里
                    graph.update_state(config, {"messages": [f"user: {text}"]})
                    print(f"[写入记忆] 用户({user_id}): {text}")
                    await websocket.send_json({"status": "ok", "msg": "用户消息已写入"})

                elif role == "agent":
                    # 客服发的消息，加上专属前缀写进记忆，让大模型以后知道这是人说的
                    graph.update_state(config, {"messages": [f"human_assist: {text}"]})
                    print(f"[写入记忆] 客服 -> 用户({user_id}): {text}")
                    await websocket.send_json({"status": "ok", "msg": "客服消息已写入"})

            # 结束对话使用Command唤醒图
            elif action == "end":
                print(f"\n[服务端] 🚨 收到结束指令，正在唤醒用户 {user_id} 的图...")
                wrap_up_note = text if text else "人工服务已结束"

                graph.invoke(Command(resume=wrap_up_note), config=config)

                await websocket.send_json({"status": "chat_ended", "msg": "大模型已重新接管"})
                break

    except WebSocketDisconnect:
        print(f"[服务端] ❌ 用户 {user_id} 的连接已断开。")
    except Exception as e:
        print(f"[服务端] ⚠️ 发生异常: {e}")


if __name__ == "__main__":
    print("🚀 启动人工客服 WebSocket 服务...")
    # 注意：如果你的主程序占用了 8000 端口，这里可以改成 8001 或其他端口
    uvicorn.run(app, host="127.0.0.1", port=8000)
