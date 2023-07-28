import logging
import sys

from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex

import custom_embed

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.13/examples/vector_stores/SimpleIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = custom_embed.embed_azure()  # Embedding Model

# ------------------------------
# ■ Load data
# ------------------------------
documents = SimpleDirectoryReader('../../../data').load_data()

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