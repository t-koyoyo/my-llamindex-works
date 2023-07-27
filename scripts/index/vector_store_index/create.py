import logging
import sys

from llama_index import SimpleDirectoryReader, VectorStoreIndex

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


documents = SimpleDirectoryReader('../../../data').load_data()
index = VectorStoreIndex.from_documents(documents, show_progress=True)

index.storage_context.persist('../../../storages/vector_store_index')