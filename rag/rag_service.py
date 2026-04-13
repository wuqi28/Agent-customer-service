from langchain_core.runnables import RunnablePassthrough

from rag.vector_store import VectorStoreService
from factory.llm_factory import qwen_chat_factory
from prompts.load_prompts import RAG_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class RagService:
    def __init__(self):
        self.vs = VectorStoreService()
        self.retriever = self.vs.get_retriever()
        self.model = qwen_chat_factory.generator()
        self.prompt = RAG_PROMPT
        self.rag_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt),
                ("human", "{input}"),
            ]
        )

    def ask(self, query):
        def format_docs(docs):
            context = ""
            count = 1
            for doc in docs:
                context += f"[参考资料{count}]:内容:{doc.page_content} 元数据:{doc.metadata}"
                count += 1
            return context

        chain = (
                {
                    "context": self.retriever | format_docs,
                    "input": RunnablePassthrough()
                }
                | self.rag_prompt
                | self.model
                | StrOutputParser()
        )
        res = chain.invoke(query)
        return res


if __name__ == '__main__':
    rag_service = RagService()
    print(rag_service.ask("如何保养"))
