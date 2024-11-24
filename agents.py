from langchain_openai import OpenAIEmbeddings , ChatOpenAI
OPENAI_API_KEY= "Update your open ai key" #TODO env variable

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
route_query_structured_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=OPENAI_API_KEY)
grade_structured_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=OPENAI_API_KEY)
grade_hallucinations_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=OPENAI_API_KEY)
generation_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)






