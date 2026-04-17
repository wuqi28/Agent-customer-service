from graph.state import CustomerState
from service.order_service import OrderService


def order_agent(state: CustomerState):
    order_service = OrderService()
    order_context = order_service.ask(state["user_input"], state["user_id"])
    return {
        "messages": [f"order_agent: {order_context}"],
        "final_response": order_context
    }
