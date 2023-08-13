from datetime import datetime
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
embed_model = common.embed_langchain("intfloat/e5-large-v2")  # Embedding Model
service_context = ServiceContext.from_defaults(llm=llm_model,embed_model=embed_model)
set_global_service_context(service_context)
message = "勤怠項目の計算イメージを教えてください。"  # クエリ

# ------------------------------
# ■ Load Index
# ------------------------------
print('Load Index Start: ', datetime.now())
index = common.load_index_vector_store_faiss()
print('Load Index End: ', datetime.now())

# ------------------------------
# ■ Do Query
# ------------------------------
# query_engine = index.as_query_engine(include_text=True, response_mode="tree_summarize")

query_engine = common.load_query_engine_for_simple(index)
response = query_engine.query(message)
if stream_mode:
  response.print_response_stream()
else:
  print(str(response))

# ------------------------------
# ■ Watch Node
# ------------------------------
# print(response.source_nodes)

# ------------------------------
# ■ Do Evaluator
# ------------------------------
# from llama_index.evaluation import ResponseEvaluator
# from llama_index.evaluation import QueryResponseEvaluator

# ## 幻覚に対する反応の評価
# # バイナリ評価 -> 合成された応答がソース コンテキストに一致する場合に「YES」/「NO」を返す
# evaluator = ResponseEvaluator()
# eval_result = evaluator.evaluate(response)
# print(str(eval_result))
# # 情報源の評価 -> すべてのソース ノードに対して「YES」/「NO」が返される
# evaluator = ResponseEvaluator()
# eval_result = evaluator.evaluate_source_nodes(response)
# print(str(eval_result))

# ## 回答品質に関するクエリ + レスポンスの評価
# # バイナリ評価 -> 合成された応答がクエリとソース コンテキストに一致する場合、「YES」/「NO」を返す
# evaluator = QueryResponseEvaluator()
# eval_result = evaluator.evaluate(message, response)
# print(str(eval_result))
# # 情報源の評価 -> 各ソース ノードを調べて、各ソース ノードにクエリに対する回答が含まれているかどうかを確認
# evaluator = QueryResponseEvaluator()
# eval_result = evaluator.evaluate_source_nodes(message, response)
# print(str(eval_result))