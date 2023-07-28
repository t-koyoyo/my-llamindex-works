# ---------------------------------
# ■ カスタムEmbedを定義する
#   - Embedding用のモデル
# ---------------------------------

import os
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding, OpenAIEmbedding

# OpenAI
def embed_openai() -> OpenAIEmbedding:
  return OpenAIEmbedding(model="text-embedding-ada-002")

# Azure AOAI
def embed_azure() -> LangchainEmbedding:
  """
  AzureOpenAIのEmbeddingを返す
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