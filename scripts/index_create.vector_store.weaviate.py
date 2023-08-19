import logging
import sys
import weaviate
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.vector_stores import WeaviateVectorStore
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.8.1/examples/vector_stores/WeaviateIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = common.embed_azure()  # Embedding Model
client = weaviate.Client("http://weaviate:8080")

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../data")

# ------------------------------
# ■ Create index
# ------------------------------
vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context, show_progress=True)