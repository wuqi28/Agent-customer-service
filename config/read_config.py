from pathlib import Path

import yaml
import os


def load_config(yaml_filename="config.yaml"):
    """
    无论在哪个目录下运行，都能准确找到并读取 yaml 配置文件
    """
    # .parent 获取该文件所在的目录
    current_dir = Path(__file__).resolve().parent

    # 打印测试--->D:\Development\python_workspace\enterprise-customer-service
    # print(current_dir)

    # 2. 假设你的 config.yaml 和当前代码文件在同一个目录下
    # 如果 config.yaml 在上一级目录，可以写成 current_dir.parent / yaml_filename
    config_path = current_dir / yaml_filename

    # 3. 检查文件是否存在
    if not config_path.exists():
        raise FileNotFoundError(f"找不到配置文件: {config_path}")

    # 4. 读取文件
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config


config = load_config("config.yaml")

# 模型相关参数
minimax_api_key = config["llm"]["minimax_api_key"]
model = config["llm"]["model"]
base_url = config["llm"]["base_url"]

deepseek_api_key = config["route_llm"]["deepseek_api_key"]
route_model = config["route_llm"]["model"]

# md5文件路径参数
md5_file_name = config["md5_file_name"]

# Embedding模型相关参数
qwen_chat_model_name = config["qwen_chat_model_name"]
qwen_embedding_model_name = config["qwen_embedding_model_name"]

# Chroma向量数据库相关参数
collection_name = config["chroma"]["collection_name"]
persist_directory = config["chroma"]["persist_directory"]
allow_types = config["chroma"]["allow_types"]

# 文本分割器相关参数
chunk_size = config["splitter"]["chunk_size"]
chunk_overlap = config["splitter"]["chunk_overlap"]
separators = config["splitter"]["separators"]

# postgresql
db_uri = config["postgresql"]["db_uri"]
