from graph.state import CustomerState


def human_node(state: CustomerState):
    return {
        "messages": ["我是human节点的回复"],
        "final_response": "我是human节点的回复"
    }
