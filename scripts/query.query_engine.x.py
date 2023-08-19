import logging
import sys
from llama_index import ServiceContext, set_global_service_context
from llama_index.indices.postprocessor import SimilarityPostprocessor
import common

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# !! 以下は想定通りの動作をしていません。chat_engine内でコンテキストは再取得されます。
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
similarity_top_k=3                                # 類似度の高い上位何件を取得するか
stream_mode=True                                  # レスポンスをストリーミングとするかどうか
llm_model = common.llm_azure()                    # LLM Model
embed_model = common.embed_azure()                # Embedding Model
service_context = ServiceContext.from_defaults(llm=llm_model,embed_model=embed_model)
set_global_service_context(service_context)
message="締日の変更が必要な場合は？"

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_index_vector_store_simple()

# ------------------------------
# ■ Get Nodes
# ------------------------------
nodes = index.as_retriever().retrieve("時刻がずれている")
# print(nodes)
# print(len(nodes))

# ------------------------------
# ■ Filtering Nodes
# ------------------------------
processor = SimilarityPostprocessor(similarity_cutoff=0.83)
filtered_nodes = processor.postprocess_nodes(nodes)
# print(nodes)
# print(len(nodes))

# ------------------------------
# ■ Do Query
# ------------------------------
query_engine = index.as_query_engine(
  node_postprocessors=[common.CustomNodePostprocessor(nodes=nodes)],
  streaming=stream_mode,
  verbose=True
)
response = query_engine.query(message)
if stream_mode:
  response.print_response_stream()
else:
  print(str(response))