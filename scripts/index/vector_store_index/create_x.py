import logging
import os
import sys
import faiss
from pathlib import Path

from llama_index import ServiceContext, StorageContext, VectorStoreIndex, download_loader
from llama_index.schema import TextNode
from llama_index.vector_stores.faiss import FaissVectorStore

import custom_embed

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
#   -> カスタム仕様
#     -> `data` フォルダ内のファイル毎にノードを作成する
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = custom_embed.embed_azure()  # Embedding Model
index_type = "faiss"  # "simple" or "faiss"
faiss_index = faiss.IndexFlatL2(1536)     # 引数は特徴量の次元数.'text-ada-embedding-002'⇒`1536`.

# ------------------------------
# ■ Create Nodes
# ------------------------------
PagedCSVReader = download_loader("PagedCSVReader")
PDFMinerReader = download_loader("PDFMinerReader")
UnstructuredReader = download_loader("UnstructuredReader")
nodes = []
for filename in os.listdir('../../../data'):                  # ファイル名を取得
  file_path = os.path.join('../../../data', filename)         # ファイル名を結合してパスを作成
  if os.path.isfile(file_path):                               # ファイルの有無を確認
    filename, file_extension = os.path.splitext(file_path)
    if file_extension=='.csv':
      documents = PagedCSVReader(encoding="utf-8").load_data(file=Path(file_path))
      node = TextNode(text=''.join(document.text for document in documents), id_=filename)
      nodes.append(node)
    if file_extension=='.docx' or file_extension=='.html' or file_extension=='.txt':
      documents = UnstructuredReader().load_data(file=Path(file_path))
      node = TextNode(text=''.join(document.text for document in documents), id_=filename)
      nodes.append(node)
    if file_extension=='.pdf':
      documents = PDFMinerReader().load_data(file=Path(file_path))
      node = TextNode(text=''.join(document.text for document in documents), id_=filename)
      nodes.append(node)

# ------------------------------
# ■ Create index
# ------------------------------
index = None
if index_type == "simple":
  service_context = ServiceContext.from_defaults(embed_model=embed_model)
  index = VectorStoreIndex(nodes=nodes, service_context=service_context, show_progress=True)
if index_type == "faiss":
  vector_store = FaissVectorStore(faiss_index=faiss_index)
  storage_context = StorageContext.from_defaults(vector_store=vector_store)
  service_context = ServiceContext.from_defaults(embed_model=embed_model)
  index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, service_context=service_context, show_progress=True)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/vector_store_index/x-'+index_type)