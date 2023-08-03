# ---------------------------------
# カスタムLLMを定義する
# ---------------------------------

import os
import openai

from llama_index.llms import AzureOpenAI

# OpenAI
def llm_openai():
  pass

# Azure AOAI
def llm_azure():
  """
  AzureOpenAIのLLM Modelを利用する場合
    -> model : text-davinci-003 | gpt-35-turbo | gpt-35-turbo-16k
    -> engine: text-davinci-003_base | gpt-35-turbo_base | gpt-35-turbo-16k_base
  """
  openai.api_key = os.environ["AOAI_API_KEY"]
  openai.api_base = os.environ["AOAI_API_HOST"]
  openai.api_type = "azure"
  openai.api_version = "2023-05-15"

  return AzureOpenAI(
    model="gpt-35-turbo-16k",
    temperature=0,
    max_tokens=800,
    engine="gpt-35-turbo-16k_base"
  )
