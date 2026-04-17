from langchain_core.output_parsers import StrOutputParser

from factory.llm_factory import minimax_chat_factory
from prompts.load_prompts import SUMMARIZE_PROMPT
from langchain_core.prompts import PromptTemplate


class SummarizeService:
    def __init__(self):
        self.model = minimax_chat_factory.generator()
        self.prompt = SUMMARIZE_PROMPT
        self.system_prompt = PromptTemplate.from_template(self.prompt)

    def summarize(self, messages):
        chain = self.system_prompt | self.model | StrOutputParser()
        res = chain.invoke({
            "history": str(messages)
        })

        return res


if __name__ == '__main__':
    service = SummarizeService()
    res = service.summarize(['user: 你好', 'intent: 用户输入为简单的日常问候"你好"，属于典型的闲聊/问候场景，与任何具体业务需求无关', 'chat_agent: 您好！我是专属智能客服。请问有什么订单或产品问题需要我为您解答？', 'user: 你好', 'intent: 用户输入为简单的问候语"你好"，属于日常闲聊/问候范畴，语义极其明确，没有任何业务意图', 'chat_agent: 您好！看来您可能有业务需要咨询，有什么我可以帮您的吗？', 'user: 你好', 'intent: 用户输入为简单的问候语"你好"，属于日常闲聊/问候范畴，与具体业务无关', 'chat_agent: 您好！已收到您的多次问候，若有订单查询、产品咨询或售后问题，请随时告诉我，我会立即为您处理。', 'user: 你好', 'intent: 用户输入为简单的日常问候"你好"，属于典型的闲聊/问候场景，与任何具体业务需求无关', 'chat_agent: 您好！检测到您多次发送“你好”，请问是遇到系统问题，还是有具体的业务需要协助？我会全力为您解决。', 'user: 你好呀', 'intent: 用户输入为日常问候语"你好呀"，属于典型的闲聊/问候场景，与具体业务无关', 'chat_agent: 您好呀！注意到您多次打招呼，是不是在尝试联系客服？如果有订单、产品或售后问题，请直接告诉我，我会马上帮您处理！', 'user: 你好', 'intent: 用户输入为简单的问候语"你好"，属于日常闲聊/问候范畴，与具体业务无关', 'chat_agent: 您好！系统已多次收到您的问候，若您有任何业务需求（如订单查询、产品咨询等），请直接说明，我会立即为您服务！', 'user: 你好，请帮我查询一下我最新的订单情况', 'intent: 用户明确要求查询订单情况，属于订单业务范畴。虽然用户以"你好"开头，但核心意图是查询订单，根据冲突处理原则应优先归类为业务意图。用户没有提供具体订单号，所以置信度略低于1.0。', 'order_agent: ', 'user: 请帮我查询一下我最新的订单情况', 'intent: 用户明确要求查询订单情况，属于订单业务范畴，但未提供具体订单号', 'order_agent: ', 'user: 你好，在吗', 'intent: 用户输入为日常问候语"你好，在吗"，属于典型的闲聊/问候场景，与具体业务无关', 'chat_agent: 您好！我在的。请问您方便提供一下账号或订单号吗？我会立即为您查询最新订单状态。'])
    print(res)


