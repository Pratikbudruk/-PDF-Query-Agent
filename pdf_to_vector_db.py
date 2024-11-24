from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor
from utils import create_vectorstore
from typing import List
import asyncio


async def load_and_split_pdfs(pdf_paths: List[str], chunk_size: int = 1024, chunk_overlap: int = 0):
    """
    Asynchronously loads and splits PDF documents into chunks.

    Args:
        pdf_paths (List[str]): List of paths to PDF files.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap between chunks.

    Returns:
        List[dict]: A list of document chunks.
    """

    def process_pdfs():
        docs = [PyMuPDFLoader(pdf_path).load() for pdf_path in pdf_paths]
        docs_list = [item for sublist in docs for item in sublist]
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(docs_list)

    # Run the blocking function in a thread pool
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, process_pdfs)
    return result


async def process_pdfs_and_create_retriever(pdf_paths: List[str]):
    doc_splits = await load_and_split_pdfs(pdf_paths)
    retriever = create_vectorstore(doc_splits, "rag-chroma")
    return retriever
