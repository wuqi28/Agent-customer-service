from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from config.read_config import deepseek_api_key, route_model
from pydantic import BaseModel, Field
from prompts.load_prompts import ROUTER_PROMPT
from graph.state import CustomerState
from factory.llm_factory import deepseek_chat_factory


# 定义结构化输出
class RouterOutput(BaseModel):
    """意图识别的输出结构"""
    intent: str = Field(description="意图类别: faq, order, complaint, escalation")
    confidence: float = Field(description="分类置信度, 0到1之间的浮点数")
    reason: str = Field(description="简短说明分类理由")


def router_node(state: CustomerState):
    # 加载提示词
    intent_prompt = ChatPromptTemplate.from_messages([
        ("system", ROUTER_PROMPT),
        ("human", "{user_input}")
    ])

    # 初始化模型
    llm = deepseek_chat_factory.generator(temperature=0.0, max_tokens=512)

    # 绑定提示词
    structured_llm = llm.with_structured_output(RouterOutput)

    router_chain = intent_prompt | structured_llm

    res = router_chain.invoke({"user_input": state["user_input"]})

    return {
        "messages": [f"User: {state['user_input']}", f"intent: {res.reason}"],
        "intent": res.intent,
        "confidence": res.confidence
    }
