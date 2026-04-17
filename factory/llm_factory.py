from abc import ABC, abstractmethod
from typing import Optional, Union

# LangChain 核心基类
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

# 具体的模型类
from langchain_deepseek import ChatDeepSeek
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

from config.read_config import deepseek_api_key, route_model, qwen_embedding_model_name, qwen_chat_model_name
from config.read_config import minimax_api_key, model, base_url


class BaseModelFactory(ABC):
    """模型工厂抽象基类，规范所有子类必须实现 generator 方法"""

    @abstractmethod
    def generator(self, **kwargs) -> Optional[Union[BaseChatModel, Embeddings]]:
        """
        生成模型实例。
        加入 **kwargs 允许在生成模型时动态传入业务参数（如 temperature）。
        """
        pass


class DeepseekChatModelFactory(BaseModelFactory):
    """对话大模型工厂：负责实例化 DeepSeek 等底层对话模型"""

    def generator(self, **kwargs) -> BaseChatModel:
        # 使用 kwargs 接收业务层传入的动态参数，并设置默认值
        temperature = kwargs.get("temperature", 0.0)
        max_tokens = kwargs.get("max_tokens", None)

        return ChatDeepSeek(
            api_key=deepseek_api_key,
            model=route_model,
            temperature=temperature,
            max_tokens=max_tokens
        )


class QwenChatModelFactory(BaseModelFactory):
    """
    千问大模型工厂，用于RAG和Chat
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=qwen_chat_model_name,
            temperature=0
        )


class MinimaxChatModelFactory(BaseModelFactory):

    def generator(self, **kwargs) -> Optional[BaseChatModel | Embeddings]:
        return ChatOpenAI(
            model=model,
            api_key=minimax_api_key,
            base_url=base_url,
            temperature=0
        )


class DashScopeEmbeddingsFactory(BaseModelFactory):
    """
    Embedding大模型
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=qwen_embedding_model_name)


deepseek_chat_factory = DeepseekChatModelFactory()
dashscope_embedding_factory = DashScopeEmbeddingsFactory()
qwen_chat_factory = QwenChatModelFactory()
minimax_chat_factory = MinimaxChatModelFactory()
