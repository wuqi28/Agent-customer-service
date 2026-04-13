from langchain_core.output_parsers import StrOutputParser
from factory.llm_factory import qwen_chat_factory
from prompts.load_prompts import CHAT_PROMPT
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage


class ChatService:
    def __init__(self):
        self.chat_model = qwen_chat_factory.generator()
        self.system_prompt = CHAT_PROMPT
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("history"),
                ("human", "{input}")
            ]
        )

    def ask(self, user_input, history):
        document_history = []  # 把历史消息数组拼接为list[Document]
        AGENT_PREFIXES = ("chat_agent:", "faq_agent:", "human_agent:", "order_agent:")
        for msg in history:
            if isinstance(msg, str):
                if msg.startswith("User:"):
                    document_history.append(HumanMessage(content=msg.replace("User:", "").strip()))
                elif msg.startswith(AGENT_PREFIXES):
                    reply_content = msg.split(":", 1)[-1].strip()
                    document_history.append(AIMessage(content=reply_content))
            else:
                document_history.append(msg)

        chain = self.chat_prompt | self.chat_model | StrOutputParser()
        res = chain.invoke({
            "input": user_input,
            "history": document_history
        })
        return res


if __name__ == '__main__':
    chat_service = ChatService()
    res = chat_service.ask("请问你记得我是谁吗", ['User: 你好', 'intent: 用户输入为简单的问候语"你好"，属于日常闲聊/问候范畴，与具体业务无关', 'chat_agent: 您好！我是专属智能客服。请问在订单、退换货或产品使用方面，有什么我可以帮您的吗？', 'User: 我是小明', 'intent: 用户仅提供姓名"小明"，属于日常社交性质的自我介绍，无具体业务需求', 'chat_agent: 您好，小明！我是专属智能客服。请问在订单、退换货或产品使用方面，有什么我可以帮您的吗？'])
    print(res)



