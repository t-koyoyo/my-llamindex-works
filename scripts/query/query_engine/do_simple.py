import logging
import sys
from llama_index import ServiceContext, set_global_service_context

import load_index
import custom_embed
import custom_llm

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
similarity_top_k=5                                # 類似度の高い上位何件を取得するか
stream_mode=False                                 # レスポンスをストリーミングとするかどうか
llm_model = custom_llm.llm_azure()                # LLM Model
embed_model = custom_embed.embed_azure()          # Embedding Model
service_context = ServiceContext.from_defaults(
  llm=llm_model,
  embed_model=embed_model
)
set_global_service_context(service_context)

# ------------------------------
# ■ Load Index
# ------------------------------
index = load_index.load_vector_store_index_simple()

# ------------------------------
# ■ Do Query
# ------------------------------
query_engine = index.as_query_engine(streaming=stream_mode, verbose=True)
response = query_engine.query("ルフィと最初に仲間になったのは誰？")
if stream_mode:
  response.print_response_stream()
else:
  print(str(response))