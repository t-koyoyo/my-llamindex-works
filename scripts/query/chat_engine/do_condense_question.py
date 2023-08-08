import logging
import sys
from llama_index import ServiceContext, set_global_service_context
from llama_index.llms import ChatMessage, MessageRole
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.21/examples/chat_engine/chat_engine_condense_question.html
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
message = '安倍晋三はいつ死んだ？'
chat_history = [
  # ChatMessage(role=MessageRole.USER,      content='打ち忘れ修正ボタンは何？'),
  # ChatMessage(role=MessageRole.ASSISTANT, content='「打ち忘れ修正」ボタンは、未処理データがある場合に表示されるボタンです。このボタンをクリックすることで、打刻漏れや誤った打刻を修正することができます。'),
]

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_vector_store_index_simple()

# ------------------------------
# ■ Do Query
# ------------------------------
chat_engine = index.as_chat_engine(
  chat_mode='condense_question',
  similarity_top_k=similarity_top_k,
  condense_question_prompt=common.custom_prompt_condense_question_prompt(),
  verbose=True,
)
response = None
if stream_mode:
  response = chat_engine.stream_chat(message=message, chat_history=chat_history)
  response.print_response_stream()
else:
  response = chat_engine.chat(message=message, chat_history=chat_history)
  print(str(response))

# ------------------------------
# ■ Add Remarks
# ------------------------------
print(response.source_nodes)    # 埋め込み回答に使用したコンテキスト情報