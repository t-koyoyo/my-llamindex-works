import logging
import sys
import faiss
from llama_index import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
#   - .env > OPENAI_API_KEY/OPENAI_API_HOST
# https://gpt-index.readthedocs.io/en/v0.7.13/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------