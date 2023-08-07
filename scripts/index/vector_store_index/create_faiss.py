import logging
import sys
import faiss

from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore

import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.20/examples/vector_stores/FaissIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings Constants
#   - faiss.IndexFlatL2  : ユークリッド距離（L2距離）を使用して全探索を行う（精度が高い）
#   - faiss.IndexFlatIP  : 内積（IP）を使用して全探索を行う（精度が高い）
#   - faiss.IndexIVFFlat : 大規模なデータセットに対する検索を高速化する（精度は若干低下）
#   - faiss.IndexIVFPQ   : メモリ使用量が大幅に削減され、検索速度が向上する（精度は若干低下）
# ------------------------------
embed_model = common.embed_azure()  # Embedding Model
faiss_index = faiss.IndexFlatL2(1536)     # 引数は特徴量の次元数.'text-ada-embedding-002'⇒`1536`.

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../../../data")

# ------------------------------
# ■ Create index
# ------------------------------
vector_store = FaissVectorStore(faiss_index=faiss_index)
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
index.storage_context.persist('../../../storages/vector_store_index/faiss')