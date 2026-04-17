from graph.state import CustomerState
from service.chat_service import ChatService
from service.summarize_service import SummarizeService


def chat_node(state: CustomerState):
    chat_service = ChatService()
    if len(state["messages"]) >= 20:
        summarize_text = SummarizeService.summarize(state["messages"])
        state["summarize_text"] = summarize_text
        messages = [state["summarize_text"]]
    else:
        messages = state["messages"]
    res = chat_service.ask(
        user_input=state["user_input"],
        history=messages,
    )

    return {
        "messages": [f"chat_agent: {res}"],
        "final_response": res
    }
