from graph.state import CustomerState
from rag.rag_service import RagService


def faq_agent(state: CustomerState):
    rag_service = RagService()
    faq_res = rag_service.ask(state["user_input"])

    return {
        "messages": [f"faq_agent: {faq_res}"],
        "final_response": faq_res
    }
