import logging
import sys
from llama_index import ServiceContext, set_global_service_context
from llama_index.indices.postprocessor import SimilarityPostprocessor
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
stream_mode=True                                  # レスポンスをストリーミングとするかどうか
llm_model = common.llm_azure()                    # LLM Model
embed_model = common.embed_azure()                # Embedding Model
service_context = ServiceContext.from_defaults(llm=llm_model,embed_model=embed_model)
set_global_service_context(service_context)
message="日付切換の方法は？"
chat_history=[]

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_index_vector_store_simple()

# ------------------------------
# ■ Get Nodes
# ------------------------------
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve(message)
print(nodes)

# ------------------------------
# ■ Filtering Nodes
# ------------------------------
# processor = SimilarityPostprocessor(similarity_cutoff=0.83)
# nodes = processor.postprocess_nodes(nodes)
# print(nodes)

#1->ノードを取得
#2->ノードをフィルタリング
#3->ノードをコンテキストとしてLLMへ質問する




# from llama_index.indices.postprocessor import SimilarityPostprocessor
# processor = SimilarityPostprocessor(similarity_cutoff=0.83)
# filtered_nodes = processor.postprocess_nodes(nodes)
# print(filtered_nodes)

# ------------------------------
# ■ Do Query
# ------------------------------
chat_engine = index.as_chat_engine(chat_mode="context",node_postprocessors=nodes,verbose=True)
if stream_mode:
  response = chat_engine.stream_chat(message=message, chat_history=chat_history)
  response.print_response_stream()
else:
  response = chat_engine.chat(message=message, chat_history=chat_history)
  print(str(response))