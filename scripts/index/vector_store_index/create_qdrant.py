import logging
import sys
import faiss
import qdrant_client

from llama_index import ServiceContext, SimpleDirectoryReader, StorageContext, VectorStoreIndex, download_loader
from llama_index.vector_stores.qdrant import QdrantVectorStore

import custom_embed

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.19/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings Constants
# ------------------------------
embed_model = custom_embed.embed_azure()  # Embedding Model
client = qdrant_client.QdrantClient(path='../../../storages/vector_store_index/qdrant')

# ------------------------------
# ■ Load data
# ------------------------------
DocxReader = download_loader("DocxReader")
PDFMinerReader = download_loader("PDFMinerReader")
UnstructuredReader = download_loader('UnstructuredReader')
dir_reader = SimpleDirectoryReader('../../../data', file_extractor={
  ".docx": DocxReader(),
  ".pdf": PDFMinerReader(),
  ".html": UnstructuredReader(),
})
documents = dir_reader.load_data()

# ------------------------------
# ■ Create index
# ------------------------------
vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(
  documents=documents,
  storage_context=storage_context,
  service_context=service_context,
  show_progress=True
)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/vector_store_index/qdrant')