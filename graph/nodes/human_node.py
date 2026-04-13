from graph.state import CustomerState
from langgraph.types import interrupt


def human_node(state: CustomerState):
    """
    人工介入节点：只负责挂起图，等待人工处理完毕后重置状态
    """
    print("⏸️ [LangGraph] 图已挂起，等待 WebSocket 人工介入...")

    wrap_up_note = interrupt({
        "action": "open_websocket_chat",
        "reason": state.get("intent"),
        "status": "waiting_for_human"
    })

    print(f"▶️ [LangGraph] 图被唤醒！人工服务总结: {wrap_up_note}")

    return {
        "requires_human": False,
        "needs_approval": False,
        "messages": [f"human_agent: {wrap_up_note}"],
        "final_response": wrap_up_note
    }
