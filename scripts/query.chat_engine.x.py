import logging
import sys
from llama_index import PromptHelper, ServiceContext, set_global_service_context
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/latest/examples/chat_engine/chat_engine_repl.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
similarity_top_k=3                                # 類似度の高い上位何件を取得するか
stream_mode=True                                  # レスポンスをストリーミングとするかどうか
llm_model = common.llm_azure()                    # LLM Model
embed_model = common.embed_azure()                # Embedding Model
prompt_helper = PromptHelper(
  context_window=16000,                           # LLMが一度に処理できるトークンの最大数（入力+出力）
  num_output=4000,                                # LLMからの最大出力トークン数
  # chunk_overlap_ratio=0.1,
  # chunk_size_limit=None
)
service_context = ServiceContext.from_defaults(
  llm=llm_model,
  embed_model=embed_model,
  prompt_helper=prompt_helper
)
set_global_service_context(service_context)

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_index_vector_store_simple()


#1->ノードを取得
#2->ノードをフィルタリング
#3->ノードをコンテキストとしてLLMへ質問する


retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve('日付切換自国の設定について参考情報を教えて')
print(nodes)

from llama_index.indices.postprocessor import SimilarityPostprocessor
processor = SimilarityPostprocessor(similarity_cutoff=0.83)
filtered_nodes = processor.postprocess_nodes(nodes)
print(filtered_nodes)

# ------------------------------
# ■ Do Query
# ------------------------------
# chat_engine = index.as_chat_engine(chat_mode='condense_question', similarity_top_k=similarity_top_k, verbose=True)
# if stream_mode:
#   streaming_response = chat_engine.stream_chat("田中航陽は結婚している？", chat_history=["田中航陽は結婚している？"])
#   for token in streaming_response.response_gen:
#     print(token, end="")
#   print(streaming_response.source_nodes)  
#   print(streaming_response.source_nodes[0])
#   print(streaming_response.source_nodes[0].node)
#   print(streaming_response.source_nodes[0].node.id_)
#   print(streaming_response.source_nodes[0].node.text)
#   print(streaming_response.source_nodes[0].score)
# else:
#   response = chat_engine.chat("安倍晋三はいつ死んだ？")
#   print(str(response))
