from llama_index.tools import FunctionTool
from llama_index.llms import OpenAI
from llama_index.agent import ReActAgent


# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.8.16/core_modules/agent_modules/agents/usage_pattern.html
# ------------------------------

# define sample Tool
def multiply(a: int, b: int) -> int:
  """2つの整数を乗算し、結果の整数を返します"""
  return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

# initialize llm
llm = OpenAI(model="gpt-3.5-turbo")

# initialize ReAct agent
agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)

agent.chat("2123 * 215123 は何ですか？")