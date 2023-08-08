import logging
import sys
from llama_index import ServiceContext, set_global_service_context
from llama_index.chat_engine import SimpleChatEngine
import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.21/examples/chat_engine/chat_engine_repl.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
llm_model = common.llm_azure()                    # LLM Model
embed_model = common.embed_azure()                # Embedding Model
service_context = ServiceContext.from_defaults(llm=llm_model,embed_model=embed_model)
set_global_service_context(service_context)

# ------------------------------
# ■ Load Index
# ------------------------------
index = common.load_vector_store_index_simple()

# ------------------------------
# ■ Do Query
# ------------------------------
chat_engine = SimpleChatEngine.from_defaults()
chat_engine.chat_repl()