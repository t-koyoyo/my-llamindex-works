import logging
import sys

from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex, download_loader

import custom_embed

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.14/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = custom_embed.embed_azure()  # Embedding Model

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