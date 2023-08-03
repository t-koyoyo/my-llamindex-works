import logging
import sys
from llama_index import PromptHelper, ServiceContext, set_global_service_context
from llama_index.llms import ChatMessage, MessageRole

import load_index
import custom_embed
import custom_llm

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/latest/examples/chat_engine/chat_engine_repl.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
similarity_top_k=3                                # 類似度の高い上位何件を取得するか
stream_mode=True                                  # レスポンスをストリーミングとするかどうか
llm_model = custom_llm.llm_azure()                # LLM Model
embed_model = custom_embed.embed_azure()          # Embedding Model
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
index = load_index.load_vector_store_index_simple()

# ------------------------------
# ■ Do Query
# ------------------------------
from llama_index.indices.postprocessor import SimilarityPostprocessor
chat_engine = index.as_chat_engine(
  chat_mode='context',
  similarity_top_k=similarity_top_k,
  verbose=True,
  node_postprocessors=SimilarityPostprocessor(similarity_cutoff=0.75).postprocess_nodes(index.as_retriever().retrieve("日付切換時刻の考え方"))
)
if stream_mode:
  streaming_response = chat_engine.stream_chat("参照情報を教えて", [
    ChatMessage(
      role=MessageRole.USER,
      content='打ち忘れ修正ボタンは何？'
    ),
    ChatMessage(
      role=MessageRole.ASSISTANT,
      content='「打ち忘れ修正」ボタンは、未処理データがある場合に表示されるボタンです。このボタンをクリックすることで、打刻漏れや誤った打刻を修正することができます。'
    ),
    ChatMessage(
      role=MessageRole.USER,
      content='どのような条件で表示される？'
    ),
    ChatMessage(
      role=MessageRole.ASSISTANT,
      content='「打ち忘れ修正」ボタンが表示される条件は以下の通りです：\n1. 未処理ケースであること（共通設定で「出退勤の打刻が揃っていない日を赤くする」が選択されている場合は対象外）\n2. 打ち忘れケースであること\n3. 時刻逆転ケースであること\n\nこれらの条件が満たされると、「打ち忘れ修正」ボタンが表示されます。'
    ),
    ChatMessage(
      role=MessageRole.USER,
      content='日本の首相はだれ？'
    ),
    ChatMessage(
      role=MessageRole.ASSISTANT,
      content='現在の日本の首相は菅義偉（すが・よしひで）です。'
    ),
    ChatMessage(
      role=MessageRole.USER,
      content='ICカード登録が終わった'
    ),
    ChatMessage(
      role=MessageRole.ASSISTANT,
      content='ICカードの登録が終わったら、次に以下の手順を実行してください：\n\n1. 従業員の出退勤のデータを受信してください。これにより、ICカードの打刻情報がシステムに反映されます。\n\n登録が完了したICカードを使用して出退勤を行う際には、ICカードをICレコーダーにかざして正しく打刻されるようにしてください。'
    ),
    ChatMessage(
      role=MessageRole.USER,
      content='日付切換時刻はどうやって設定する？'
    ),
    ChatMessage(
      role=MessageRole.ASSISTANT,
      content='日付切換時刻の設定方法は、集計ソフトとタイムレコーダーで異なります。\n\n【集計ソフトの場合】\n日付切換時刻は、1日の処理日を決める時刻です。出勤・退勤の打刻が日付切換時刻内で行われるように設定します。\n\n例えば、出勤打刻が5:00より早い場合や5:00を過ぎる定時がある場合は、拡張1や拡張2で設定する必要があります。\n\n具体的な設定方法は、集計ソフトのマニュアルやサポート資料を参照してください。\n\n【タイムレコーダーの場合】\nタイムレコーダーの日付切換時刻は、タイムカードの日付段が切り替わる時刻を設定する機能です。ICカードの場合は設定不要です。\n\n例えば、日付切換時刻を5:00に設定すると、5:00から翌日4:59までの出退勤が同日に印字され、翌日5:00になると翌日段に印字されます。\n\n具体的な設定方法は、タイムレコーダーの取扱説明書やサポート資料を参照してください。'
    ),
  ])
  for token in streaming_response.response_gen:
    print(token, end="")
  print(streaming_response.source_nodes)  
  print(streaming_response.source_nodes[0])
  print(streaming_response.source_nodes[0].node)
  print(streaming_response.source_nodes[0].node.id_)
  print(streaming_response.source_nodes[0].node.text)
  print(streaming_response.source_nodes[0].score)
else:
  response = chat_engine.chat("安倍晋三はいつ死んだ？")
  print(str(response))
