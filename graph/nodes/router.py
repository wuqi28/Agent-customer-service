from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from config.read_config import deepseek_api_key, route_model
from pydantic import BaseModel, Field
from prompts.load_prompts import ROUTER_PROMPT


# 定义结构化输出
class RouterOutput(BaseModel):
    """意图识别的输出结构"""
    intent: str = Field(description="意图类别: faq, order, complaint, escalation")
    confidence: float = Field(description="分类置信度, 0到1之间的浮点数")
    reason: str = Field(description="简短的分类理由")


# 加载提示词
intent_prompt = ChatPromptTemplate.from_messages([
    ("system", ROUTER_PROMPT),
    ("human", "{user_input}")
])

# 初始化模型
llm = ChatDeepSeek(
    api_key=deepseek_api_key,
    model=route_model,
    temperature=0
)

# 绑定提示词
structured_llm = llm.with_structured_output(RouterOutput)

router_chain = intent_prompt | structured_llm

res = router_chain.invoke({"user_input": "你好，我的快递单号是 SF123456，帮我查查到哪了"})

print(res)
