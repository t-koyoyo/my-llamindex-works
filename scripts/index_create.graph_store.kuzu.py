import logging
import os
import sys
import kuzu
from pyvis.network import Network
from llama_index import KnowledgeGraphIndex, ServiceContext, StorageContext
from llama_index.graph_stores import KuzuGraphStore
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.8.1/examples/index_structs/knowledge_graph/KuzuGraphDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
llm_model = common.llm_azure()      # LLM Model
embed_model = common.embed_azure()  # Embedding Model

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../data")

# ------------------------------
# ■ Create Folder
# ------------------------------
if not os.path.exists('../storages/graph_store/kuzu'):
  os.makedirs('../storages/graph_store/kuzu')

# ------------------------------
# ■ Create index
# ------------------------------
db = kuzu.Database(database_path='../storages/graph_store/kuzu/db')
graph_store = KuzuGraphStore(db)
storage_context = StorageContext.from_defaults(graph_store=graph_store)
service_context = ServiceContext.from_defaults(llm=llm_model, chunk_size=512, embed_model=embed_model)
index = KnowledgeGraphIndex.from_documents(
  documents,
  storage_context=storage_context,
  service_context=service_context,
  max_triplets_per_chunk=2,             # 抽出するトリプレットの最大数
  include_embeddings=True,              # インデックスに埋め込みを含めるかどうか
  show_progress=True,
)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../storages/graph_store/kuzu')

# ------------------------------
# ■ Create Visualizing the Graph
# ------------------------------
g = index.get_networkx_graph()
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show("../storages/graph_store/kuzu/visual-graph.html")