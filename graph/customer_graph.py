from langgraph.graph import StateGraph, START, END
from graph.state import CustomerState
from graph.nodes.router import router_node
from graph.nodes.faq_agent import faq_agent
from graph.nodes.order_agent import order_agent
from graph.nodes.human_node import human_node


# 定义条件路由函数
def route_func(state: CustomerState) -> str:
    """
    根据router节点的意图识别，决定下一步去哪个节点
    :param state:
    :return:
    """
    intent = state["intent"]
    confidence = state["confidence"]

    # 置信度过低大模型都无法理解就转人工
    if confidence < 0.7:
        return "escalation"

    # 根据意图分发节点
    if intent == "faq":
        return "faq"
    elif intent == "order":
        return "order"
    elif intent in ("complaint", "escalation"):
        return "human"
    else:
        return "human"


def build_graph():
    workflow = StateGraph(CustomerState)

    workflow.add_node("router", router_node)
    workflow.add_node("faq", faq_agent)
    workflow.add_node("order", order_agent)
    workflow.add_node("human", human_node)

    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        route_func,
        {
            "faq": "faq",
            "order": "order",
            "human": "human",
        }
    )

    workflow.add_edge("faq", END)
    workflow.add_edge("order", END)
    workflow.add_edge("human", END)

    return workflow.compile()


if __name__ == '__main__':
    graph = build_graph()
    res = graph.invoke({"user_input": "帮我查询订单号12345678"})
    print(res)
