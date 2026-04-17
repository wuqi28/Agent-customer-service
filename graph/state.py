import operator
from typing import TypedDict, Annotated, List, Any


class CustomerState(TypedDict, total=False):
    """
    企业级只能客服系统全局状态
    使用 total=False
    """
    # --- 基础输入与会话信息 ---
    user_input: str
    user_id: str
    session_id: str
    summarize_text: str
    summarized_status: bool

    # --- 意图识别结果 (覆盖更新) ---
    intent: str
    confidence: float

    # --- 对话历史 (累积更新) ---
    messages: Annotated[List[str], operator.add]

    # --- 检索与工具结果 (覆盖更新) ---
    retrieved_docs: List[Any]

    # --- 流程控制与最终输出 (覆盖更新) ---
    needs_approval: bool
    requires_human: bool
    final_response: str
