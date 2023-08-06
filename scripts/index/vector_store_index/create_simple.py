import logging
import sys

from llama_index import ServiceContext, VectorStoreIndex

import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.19/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = common.embed_azure()  # Embedding Model

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../../../data")

# ------------------------------
# ■ Create index
# ------------------------------
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(
  documents=documents,
  service_context=service_context,
  show_progress=True
)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/vector_store_index/simple')