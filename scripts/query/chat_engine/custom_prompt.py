# ---------------------------------
# カスタムプロンプトを定義する
# ---------------------------------

from llama_index.prompts import Prompt

# Query > LLMへの質問（初回）
text_qa_template_str = (
  "コンテキスト情報は以下のとおりです\n"
  "---------------------\n"
  "{context_str}\n"
  "---------------------\n"
  "Using both the context information and also using your own knowledge, "
  "answer the question: {query_str}\n"
  "If the context isn't helpful, you can also answer the question on your own.\n"
)
text_qa_template = Prompt(text_qa_template_str)

# Query > LLMへの質問（2回目以降）
refine_template_str = (
  "The original question is as follows: {query_str}\n"
  "We have provided an existing answer: {existing_answer}\n"
  "We have the opportunity to refine the existing answer "
  "(only if needed) with some more context below.\n"
  "------------\n"
  "{context_msg}\n"
  "------------\n"
  "Using both the new context and your own knowledege, update or repeat the existing answer.\n"
)
refine_template = Prompt(refine_template_str)