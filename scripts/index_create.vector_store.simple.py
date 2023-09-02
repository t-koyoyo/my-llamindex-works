import logging
import sys

from llama_index import ServiceContext, VectorStoreIndex

import common

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.8.16/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = common.embed_azure()

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../data")

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Create index
# ------------------------------
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_documents(documents=documents,service_context=service_context,show_progress=True)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../storages/vector_store/simple')

## 質問生成
# from llama_index.evaluation import DatasetGenerator, QueryResponseEvaluator
# service_context = ServiceContext.from_defaults(llm=common.llm_azure(),embed_model=common.embed_azure())
# data_generator = DatasetGenerator.from_documents(documents,service_context=service_context)
# eval_questions = data_generator.generate_questions_from_nodes()
# print(eval_questions)