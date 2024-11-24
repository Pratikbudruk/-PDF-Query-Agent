import json
import aiofiles
import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
from pdf_to_vector_db import process_pdfs_and_create_retriever
from utils import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

UPLOAD_DIRECTORY = "uploaded_files"
TOP_K = 4
DEFAULT_DOCS_TO_RETRIEVE = 3
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/extract_information_from_pdf/")
async def process_pdf(
        questions: str = Form(...),
        file: UploadFile = File(...),
        description: Optional[str] = Form(None),
        check_hallucination: Optional[str] = Form(None)):
    logger.info("Received a request to process a PDF file.")
    try:
        questions_dict = json.loads(questions)
        question_list = questions_dict.get("question", [])
        print(question_list)
        if not question_list:
            raise HTTPException(status_code=400, detail="No questions found in the 'questions' parameter")
    except json.JSONDecodeError:
        logger.error("Invalid JSON format for 'questions'")
        raise HTTPException(status_code=400, detail="Invalid JSON format for 'questions'")
    except ValueError as e:
        logger.error(f"Error while parsing 'questions': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    try:
        # TODO better handling for large PDF
        logger.debug(f"Saving uploaded PDF file: {file.filename}")
        pdf_filename = file.filename
        file_path = os.path.join(UPLOAD_DIRECTORY, pdf_filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())
        logger.debug(f"File saved successfully at: {file_path}")
    except Exception as e:
        logger.error(f"File save failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")

    try:
        logger.debug("Processing PDF to create retriever.")
        retriever = await process_pdfs_and_create_retriever(pdf_paths=[file_path])
        logger.debug("Retriever created successfully.")
    except Exception as e:
        delete_file(file_path)
        logger.error(f"PDF processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

    response_dict_ = {}
    no_context_question = []

    try:
        if description:
            logger.debug("Validating questions against description.")
            for question in question_list:
                has_context = await validate_question(question, description)
                if has_context.lower() == "web_search":
                    response_dict_[question] = "Data_Not_Available"
                    no_context_question.append(question)
            logger.debug("Question validation completed.")
    except Exception as e:
        logger.error(f"Error while validating questions: {str(e)}")
        delete_file(file_path)
        raise HTTPException(status_code=500, detail=f"Error while validating questions: {str(e)}")

    try:
        logger.info("Answering questions using retriever.")
        for question in question_list:
            logger.debug(f"Answering question {question} using retriever.")
            if question not in no_context_question:
                docs = retriever.get_relevant_documents(question)[:TOP_K]
                doc_txt = "\n\n".join([docs[index].page_content for index in range(0, DEFAULT_DOCS_TO_RETRIEVE)])
                response = await handle_question(question, docs, doc_txt,
                                                 check_hallucination=check_hallucination)
                response_dict_[question] = response
                logger.debug(f"Answer to question {question} using retriever : {response}.")

        logger.info("Question answering completed.")

    except Exception as e:
        delete_file(file_path)
        raise HTTPException(status_code=500, detail="Error while answering question given pdf context")

    delete_file(file_path)

    return response_dict_
