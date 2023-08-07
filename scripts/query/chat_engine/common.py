import os
import openai
import qdrant_client
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding, OpenAIEmbedding, Prompt, StorageContext, load_index_from_storage
from llama_index.llms import AzureOpenAI, OpenAI
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore


## ----------------------------------------
## ■ Embedding Model
## ----------------------------------------
def embed_azure() -> LangchainEmbedding:
  """
  AOAI Embedding Model
  :return: LangchainEmbedding
  """
  os.environ["OPENAI_API_KEY"] = os.environ["AOAI_API_KEY"]
  os.environ["OPENAI_API_BASE"] = os.environ["AOAI_API_HOST"]
  os.environ["OPENAI_API_TYPE"] = "azure"
  os.environ["OPENAI_API_VERSION"] = "2023-05-15"

  return LangchainEmbedding(
    OpenAIEmbeddings(
      model="text-embedding-ada-002",
      deployment="text-embedding-ada-002_base",
    ),
    embed_batch_size=1,
  )

def embed_openai() -> OpenAIEmbedding:
  """
  OpenAI Embedding Model
  :return: OpenAIEmbedding
  """
  return OpenAIEmbedding(model="text-embedding-ada-002")


## ----------------------------------------
## ■ LLM Model
## ----------------------------------------
def llm_azure() -> AzureOpenAI:
  """
  AOAI LLM Model
    -> model : text-davinci-003 | gpt-35-turbo | gpt-35-turbo-16k
    -> engine: text-davinci-003_base | gpt-35-turbo_base | gpt-35-turbo-16k_base
  """
  openai.api_key = os.environ["AOAI_API_KEY"]
  openai.api_base = os.environ["AOAI_API_HOST"]
  openai.api_type = "azure"
  openai.api_version = "2023-05-15"

  return AzureOpenAI(
    model="gpt-35-turbo-16k",
    temperature=0,
    max_tokens=800,
    engine="gpt-35-turbo-16k_base"
  )

def llm_openai() -> OpenAI:
  """
  OpenAI LLM Model
    -> model : text-davinci-003 | gpt-3.5-turbo-0613
  """
  return OpenAI(model="gpt-3.5-turbo-0613")


## ----------------------------------------
## ■ Load Index
## ----------------------------------------
def load_vector_store_index_faiss():
  vector_store = FaissVectorStore.from_persist_dir("../../../storages/vector_store_index/faiss")
  storage_context = StorageContext.from_defaults(
    vector_store=vector_store,
    persist_dir="../../../storages/vector_store_index/faiss"
  )
  return load_index_from_storage(storage_context=storage_context)

def load_vector_store_index_qdrant():
  client = qdrant_client.QdrantClient(path='../../../storages/vector_store_index/qdrant')
  vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
  storage_context = StorageContext.from_defaults(
    vector_store=vector_store,
    persist_dir="../../../storages/vector_store_index/qdrant"
  )
  return load_index_from_storage(storage_context=storage_context)

def load_vector_store_index_simple():
  storage_context = StorageContext.from_defaults(persist_dir="../../../storages/vector_store_index/simple")
  return load_index_from_storage(storage_context=storage_context)


## ----------------------------------------
## ■ Custom Prompt
## ----------------------------------------
def custom_prompt_condense_question_prompt():
  """
  Chat Engine Custom Prompt
    -> 要約質問プロンプト
  """
  return Prompt("""\
    Given a conversation (between Human and Assistant) and a follow up message from Human, \
    rewrite the message to be a standalone question that captures all relevant context \
    from the conversation.

    <Chat History>
    {chat_history}

    <Follow Up Message>
    {question}

    <Standalone question>
  """)