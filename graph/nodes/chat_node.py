from graph.state import CustomerState
from service.chat_service import ChatService


def chat_node(state: CustomerState):
    chat_service = ChatService()
    res = chat_service.ask(
        user_input=state["user_input"],
        history=state["messages"],
    )

    return {
        "messages": [f"chat_agent: {res}"],
        "final_response": res
    }
