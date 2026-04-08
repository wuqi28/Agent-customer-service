from graph.state import CustomerState


def faq_agent(state: CustomerState):
    return {
        "messages": ["我是faq节点的回复"],
        "final_response": "我是faq节点的回复"
    }
