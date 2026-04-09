import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from config.read_config import md5_file_name


def pdf_loader(path: str, pwd=None) -> PyPDFLoader:
    return PyPDFLoader(path, pwd).load()


def text_loader(path: str) -> TextLoader:
    return TextLoader(path, encoding="utf-8").load()


def get_file_md5_hex(filepath: str):
    """
    获取文件的md5的十六进制字符串
    :return:
    """
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    md5_obj = hashlib.md5()

    chunk_size = 4096
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None


def check_md5_hex(md5_for_check: str):
    if not os.path.exists(get_abs_path(md5_file_name)):
        open(get_abs_path(md5_file_name), "w", encoding="utf-8").close()
        return False

    with open(get_abs_path(md5_file_name), "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == md5_for_check:
                return True

        return False


def add_md5_hex(md5_from_checked: str):
    with open(get_abs_path(md5_file_name), "a", encoding="utf-8") as f:
        f.write(md5_from_checked + "\n")
