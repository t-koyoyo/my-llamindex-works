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
index = load_index.load_vector_store_index_qdrant()

# ------------------------------
# ■ Do Query
# ------------------------------
chat_engine = index.as_chat_engine(chat_mode='condense_question',verbose=True)
if stream_mode:
  streaming_response = chat_engine.stream_chat("安倍晋三はいつ死んだ？")
  for token in streaming_response.response_gen:
    print(token, end="")
else:
  response = chat_engine.chat("安倍晋三はいつ死んだ？")
  print(str(response))
