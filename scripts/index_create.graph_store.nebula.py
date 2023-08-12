import logging
import os
import sys
from pyvis.network import Network
from llama_index import KnowledgeGraphIndex, ServiceContext, StorageContext
from llama_index.graph_stores import NebulaGraphStore
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.8.0/examples/index_structs/knowledge_graph/NebulaGraphKGIndexDemo.html
# ------------------------------
os.environ["NEBULA_USER"]     = "root"              # default it is "root"
os.environ["NEBULA_PASSWORD"] = "nebula"            # default it is "nebula"
os.environ["NEBULA_ADDRESS"]  = "nebula:9669"       # assumed we have NebulaGraph 3.5.0 or newer installed locally

# ------------------------------
# ■ Settings
# ------------------------------
llm_model = common.llm_azure()      # LLM Model
embed_model = common.embed_azure()  # Embedding Model
nebula_space_name     = "llam_index"      # Nebula Graph Space Name
nebula_edge_types     = ["relationship"]  # Nebula Graph Edge Types
nebula_rel_prop_names = ["relationship"]  # Nebula Graph Relationship Property Names
nebula_tags           = ["entity"]        # Nebula Graph Tags

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../data")

# ------------------------------
# ■ Create index
# ------------------------------
graph_store = NebulaGraphStore(space_name=nebula_space_name,edge_types=nebula_edge_types,rel_prop_names=nebula_rel_prop_names,tags=nebula_tags)
storage_context = StorageContext.from_defaults(graph_store=graph_store)
service_context = ServiceContext.from_defaults(llm=llm_model, chunk_size=512, embed_model=embed_model)
index = KnowledgeGraphIndex.from_documents(
  documents,
  storage_context=storage_context,
  service_context=service_context,
  max_triplets_per_chunk=10,              # 抽出するトリプレットの最大数
  include_embeddings=True,                # インデックスに埋め込みを含めるかどうか
  space_name=nebula_space_name,           # Nebula Graph Space Name
  edge_types=nebula_edge_types,           # Nebula Graph Edge Types
  rel_prop_names=nebula_rel_prop_names,   # Nebula Graph Relationship Property Names
  tags=nebula_tags,                       # Nebula Graph Tags
  show_progress=True,
)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../storages/graph_store/nebula')

# ------------------------------
# ■ Create Visualizing the Graph
# ------------------------------
g = index.get_networkx_graph()
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show("../storages/graph_store/nebula/visual-graph.html")