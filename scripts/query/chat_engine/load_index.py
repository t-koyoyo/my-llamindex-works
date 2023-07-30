import qdrant_client
from llama_index import StorageContext, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore


def load_vector_store_index_simple():
  storage_context = StorageContext.from_defaults(persist_dir="../../../storages/vector_store_index/simple")
  return load_index_from_storage(storage_context=storage_context)

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