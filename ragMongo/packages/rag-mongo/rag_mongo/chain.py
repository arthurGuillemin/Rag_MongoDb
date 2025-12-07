import os

from langchain_openai import AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Set DB

MONGO_URI = ""

DB_NAME = "langchain"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
MONGODB_COLLECTION = db[COLLECTION_NAME]


# Initialiser le modèle LLM avec les paramètres d'Azure OpenAI
llm = AzureChatOpenAI(
    openai_api_version="2023-09-01-preview",
    azure_endpoint=os.getenv('AZURE_API_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    azure_deployment=os.getenv('OPENAI_DEPLOYMENT_NAME'),
    model_name=os.getenv('OPENAI_MODEL_NAME'),
    model_version=os.getenv('OPENAI_API_VERSION')
)

# Initialiser les embeddings d'Azure OpenAI
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("azure_deployment"),
    openai_api_version=os.getenv("openai_api_version"),
)


# VectorStore
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string= ,
    namespace=DB_NAME + "." + COLLECTION_NAME,
    embedding= embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

# Initialisation du retriver
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})


# prompt
retrieve = {"context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), "question": RunnablePassthrough()}
template = """Answer the question based only on the following context: \
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

parse_output = StrOutputParser()

# création de la chaine
rag_chain = (
    retrieve
    | prompt
    | llm
    | parse_output
)

Question = rag_chain.invoke("Que doit contenir le budget previsionnel ?")
print(Question)

