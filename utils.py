import os

from typing import List, Literal
from prompts import router_prompt_text, grade_prompt_text, hallucination_prompt_text, generation_prompt
from agents import route_query_structured_llm, embeddings, grade_structured_llm, grade_hallucinations_llm, \
    generation_llm
from models import RouteQuery, GradeDocuments, GradeHallucinations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", hallucination_prompt_text),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", grade_prompt_text),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

structured_llm_router = route_query_structured_llm.with_structured_output(RouteQuery)

structured_llm_grader = grade_structured_llm.with_structured_output(GradeDocuments)
retrieval_grader_agent = grade_prompt | structured_llm_grader

structured_llm_hallucination_grader = grade_hallucinations_llm.with_structured_output(GradeHallucinations)
hallucination_grader_agent = hallucination_prompt | structured_llm_grader

rag_generation_agent = generation_prompt | generation_llm | StrOutputParser()



async def generate(docs, question) -> str:
    generation = rag_generation_agent.invoke({"context": docs, "question": question})
    if generation == "I don't know.":
        return "Data_Not_Available"
    return generation


async def validate_question(question: str, description_text: str) -> Literal["vectorstore", "web_search"]:
    """
    Validates the question and determines which datasource (vectorstore or web_search)
    should be used for answering it.

    Args:
    - question (str): The question to be routed.
   - description_text(str) : router_prompt_text

    Returns:
    - Literal["vectorstore", "web_search"]: The recommended datasource for the question.
    """

    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", f"{router_prompt_text} {description_text} Otherwise, use web-search."),
            ("human", "{question}"),
        ]
    )

    question_router_agent = route_prompt | structured_llm_router

    result =  question_router_agent.invoke({"question": question})
    return result.datasource


async def grade_retrieved_document(question: str, document_text: str) -> str:
    """
    Grades the relevance of a retrieved document based on a user question.

    Args:
    - question (str): The user question.
    - document_text (str): The retrieved document text.


    Returns:
    - str: The relevance score ('yes' or 'no').
    """
    result =  retrieval_grader_agent.invoke({"question": question, "document": document_text})
    return result.binary_score


async def grade_hallucinations(documents: List[str], generation: str) -> str:
    """
    Grades whether an LLM generation is grounded in a set of facts, checking for hallucinations.

    Args:
    - documents (List[str]): The set of facts that should support the generation.
    - generation (str): The LLM's generated response to be checked.

    Returns:
    - str: The relevance score ('yes' or 'no') indicating whether the generation is grounded in facts.
    """

    result =  hallucination_grader_agent.invoke({"documents": documents, "generation": generation})
    return result.binary_score


async def handle_question(question, docs, doc_txt, check_hallucination=False):
    binary_score = await grade_retrieved_document(question, doc_txt)
    if binary_score == "yes":
        generated_text = await generate(docs, question)
        if check_hallucination:
            hallucination_score = await grade_hallucinations(doc_txt, generated_text)
            if hallucination_score == "yes":
                return generated_text
        else:
            return generated_text
    return "Data_Not_Available"


def create_vectorstore(doc_splits: List[dict], collection_name: str, ):
    """
    Creates a vector database from document splits.

    Args:
        doc_splits (List[dict]): List of document chunks.
        openai_api_key (str): API key for OpenAI embeddings.

    Returns:
        Chroma retriever: A retriever object for querying the vector database.
    """

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name=collection_name,
        embedding=embeddings,
    )
    return vectorstore.as_retriever()


def delete_file(file_path: str):
    """
    Utility to delete a file if it exists.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete file {file_path}: {str(e)}")
