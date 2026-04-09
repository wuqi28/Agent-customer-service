import os

from langchain_chroma import Chroma
from factory.llm_factory import dashscope_embedding_factory
from config.read_config import collection_name, persist_directory, chunk_size, chunk_overlap, separators, allow_types
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from langchain_core.documents import Document

from utils.logger_handler import logger

from utils.file_tool import get_file_md5_hex, check_md5_hex, add_md5_hex, pdf_loader, text_loader


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files = []

    if not os.path.isdir(path):
        logger.warning(f'Path {path} is not a directory')
        return tuple(files)

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)


def get_file_documents(read_path: str) -> list[Document]:
    if read_path.endswith(".pdf"):
        return pdf_loader(read_path)

    if read_path.endswith(".txt"):
        return text_loader(read_path)

    return []


class VectorStoreService:
    def __init__(self):
        # 向量存储数据库
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=dashscope_embedding_factory.generator(),
            persist_directory=get_abs_path(persist_directory)
        )

        # 文档分割器
        self.text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

    def insert_documents_for_chroma(self):
        allowed_files_path = listdir_with_allowed_type(get_abs_path("data"), tuple(allow_types))

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f'[加载知识库]{path}内容已经存在知识库内，跳过')
                continue

            documents = get_file_documents(path)

            if not documents:
                logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                continue

            split_documents = self.text_spliter.split_documents(documents)

            self.vector_store.add_documents(split_documents)

            add_md5_hex(md5_hex)


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.insert_documents_for_chroma()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    print(res)
