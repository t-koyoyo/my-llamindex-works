import logging
import sys
from pyvis.network import Network
from llama_index import KnowledgeGraphIndex, ServiceContext, StorageContext
from llama_index.graph_stores import SimpleGraphStore
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.22/examples/index_structs/knowledge_graph/KnowledgeGraphDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
llm_model = common.llm_azure()      # LLM Model
embed_model = common.embed_azure()  # Embedding Model

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../../../data")

# ------------------------------
# ■ Create index
# ------------------------------
graph_store = SimpleGraphStore()
storage_context = StorageContext.from_defaults(graph_store=graph_store)
service_context = ServiceContext.from_defaults(llm=llm_model, chunk_size=512, embed_model=embed_model)
index = KnowledgeGraphIndex.from_documents(
  documents,
  max_triplets_per_chunk=10,
  storage_context=storage_context,
  service_context=service_context,
  include_embeddings=True,
  show_progress=True,
)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/knowledge_graph_index/simple')

# ------------------------------
# ■ Create Visualizing the Graph
# ------------------------------
g = index.get_networkx_graph()
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show("../../../storages/knowledge_graph_index/simple/example.html")