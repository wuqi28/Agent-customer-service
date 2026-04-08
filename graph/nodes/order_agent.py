from graph.state import CustomerState


def order_agent(state: CustomerState):
    return {
        "messages": ["我是order节点的回复"],
        "final_response": "我是order节点的回复"
    }
