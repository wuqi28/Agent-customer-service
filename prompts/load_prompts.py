from pathlib import Path


def _load_prompt_text(filename: str) -> str:
    """
    内部辅助函数：根据文件名读取 prompts 目录下的 txt 文件
    """
    # 1. 获取当前文件所在的绝对路径
    current_dir = Path(__file__).resolve().parent

    # 2. 路径拼接
    prompt_file_path = current_dir / filename

    # 3. 检查文件是否存在并读取
    if not prompt_file_path.exists():
        raise FileNotFoundError(f"找不到提示词文件: {prompt_file_path}")

    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 读取 router_prompt.txt 的内容并赋值给 ROUTER_PROMPT 变量
ROUTER_PROMPT = _load_prompt_text("router_prompt.txt")
RAG_PROMPT = _load_prompt_text("rag_prompt.txt")
