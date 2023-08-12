import logging
import sys
from llama_index import ServiceContext, set_global_service_context
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
similarity_top_k=3                                # 類似度の高い上位何件を取得するか
stream_mode=False                                 # レスポンスをストリーミングとするかどうか
llm_model = common.llm_azure()                    # LLM Model
embed_model = common.embed_azure()                # Embedding Model
service_context = ServiceContext.from_defaults(llm=llm_model,embed_model=embed_model)
set_global_service_context(service_context)

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_index_graph_store_knowledge()

# ------------------------------
# ■ Do Query
# ------------------------------
query_engine = common.load_query_engine_for_knowledge_graph(index=index)
response = query_engine.query("どのタイムカードを使用したらよいですか？")
if stream_mode:
  response.print_response_stream()
else:
  print(str(response))

# ------------------------------
# ■ Watch Node
# ------------------------------
# print(response.source_nodes)