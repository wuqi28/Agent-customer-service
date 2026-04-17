import openai
import re
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent

from config.read_config import mysql_db_uri
from factory.llm_factory import minimax_chat_factory


class OrderService:
    def __init__(self):
        self.db_url = mysql_db_uri
        self.db = SQLDatabase.from_uri(mysql_db_uri)
        self.minimax = minimax_chat_factory.generator()
        self.toolkit = SQLDatabaseToolkit(
            db=self.db,
            llm=self.minimax
        )

    def ask(self, user_input, user_id):
        sql_agent = create_sql_agent(
            llm=self.minimax,
            toolkit=self.toolkit,
            verbose=True,
            agent_type="tool-calling"
        )
        try:
            res = sql_agent.invoke({"input": f"user_id: {user_id}, user_input: {user_input}"})
            raw_output = res["output"]
            clean_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL)
            return clean_output.strip()
        except openai.InternalServerError:
            return "MiniMax 服务器正在排队，请稍后再试（Error 529）。"
        except openai.RateLimitError:
            return "请求太频繁了，请稍等片刻。"
        except Exception as e:
            print(f"其他错误: {type(e).__name__} - {e}")
            return "系统开小差了，请稍后重试。"


if __name__ == '__main__':
    order_service = OrderService()
    print(order_service.ask("查询一下的我最新的订单情况", "user05"))
