import os
import openai
from langchain.embeddings import OpenAIEmbeddings
from llama_index import Document, LangchainEmbedding, OpenAIEmbedding, SimpleDirectoryReader, SimpleWebPageReader, download_loader
from llama_index.llms import AzureOpenAI, OpenAI


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
    -> model : text-davinci-003 | gpt-3.5-turbo
  """
  return OpenAI(model="text-davinci-003")


## ----------------------------------------
## ■ Load Documents
## ----------------------------------------
def load_documents_local_files(dir_path:str) -> list[Document]:
  """
  ローカル環境のファイルをドキュメントとして読み込む
  https://gpt-index.readthedocs.io/en/latest/examples/data_connectors/simple_directory_reader.html
    -> Usage:
      -> documents = load_documents.load_documents_local_files("../../../data")
  :param dir_path: directory path | e.g. "../../../data"
  """
  DocxReader = download_loader("DocxReader")
  JSONReader = download_loader("JSONReader")
  PagedCSVReader = download_loader("PagedCSVReader")
  PDFMinerReader = download_loader("PDFMinerReader")
  UnstructuredReader = download_loader('UnstructuredReader')
  return SimpleDirectoryReader(dir_path, file_extractor={
    ".csv": PagedCSVReader(),
    ".docx": DocxReader(),
    ".html": UnstructuredReader(),
    ".json": JSONReader(),
    ".pdf": PDFMinerReader(),
  }, recursive=True, required_exts=[".csv",".docx",".html",".json",".pdf"]).load_data()

def load_documents_web_page(web_pages:list[str]) -> list[Document]:
  """
  Webページをドキュメントとして読み込む
  https://gpt-index.readthedocs.io/en/latest/examples/data_connectors/WebPageDemo.html
    -> Usage:
      -> documents = load_documents.load_documents_web_page(["https://ja.wikipedia.org/wiki/ONE_PIECE"])
  :param web_pages: list of web pages | e.g. ["http://paulgraham.com/worked.html"]
  """
  return SimpleWebPageReader(html_to_text=True).load_data(web_pages)