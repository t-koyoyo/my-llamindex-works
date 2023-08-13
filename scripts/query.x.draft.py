import logging
import sys
from llama_index import LLMPredictor, ServiceContext, set_global_service_context
from llama_index.indices.query.query_transform import HyDEQueryTransform
from llama_index.query_engine.transform_query_engine import TransformQueryEngine
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
llm_predictor = LLMPredictor(llm=llm_model)
embed_model = common.embed_azure()                # Embedding Model
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,embed_model=embed_model)
set_global_service_context(service_context)
message = "どのタイムカードを使用したらよいですか？"  # クエリ

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_index_vector_store_simple()

# ------------------------------
# ■ Do Query
# ------------------------------
query_engine = index.as_query_engine()
hyde = HyDEQueryTransform(include_original=True, llm_predictor=llm_predictor)
hyde_query_engine = TransformQueryEngine(query_engine, hyde)
response = hyde_query_engine.query("Which timecard should I use?")
print(str(response))

# ------------------------------
# ■ Watch Node
# ------------------------------
# print(response.source_nodes)

# ------------------------------
# ■ Do Evaluator
# ------------------------------
from llama_index.evaluation import ResponseEvaluator
from llama_index.evaluation import QueryResponseEvaluator

## 幻覚に対する反応の評価
# バイナリ評価 -> 合成された応答がソース コンテキストに一致する場合に「YES」/「NO」を返す
evaluator = ResponseEvaluator()
eval_result = evaluator.evaluate(response)
print(str(eval_result))
# 情報源の評価 -> すべてのソース ノードに対して「YES」/「NO」が返される
evaluator = ResponseEvaluator()
eval_result = evaluator.evaluate_source_nodes(response)
print(str(eval_result))

## 回答品質に関するクエリ + レスポンスの評価
# バイナリ評価 -> 合成された応答がクエリとソース コンテキストに一致する場合、「YES」/「NO」を返す
evaluator = QueryResponseEvaluator()
eval_result = evaluator.evaluate(message, response)
print(str(eval_result))
# 情報源の評価 -> 各ソース ノードを調べて、各ソース ノードにクエリに対する回答が含まれているかどうかを確認
evaluator = QueryResponseEvaluator()
eval_result = evaluator.evaluate_source_nodes(message, response)
print(str(eval_result))