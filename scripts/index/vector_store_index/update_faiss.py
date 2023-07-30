from llama_index import SimpleDirectoryReader, download_loader

import load_index

# ------------------------------
# ■ Load data
# ------------------------------
DocxReader = download_loader("DocxReader")
PDFMinerReader = download_loader("PDFMinerReader")
UnstructuredReader = download_loader('UnstructuredReader')
dir_reader = SimpleDirectoryReader('../../../data', file_extractor={
  ".docx": DocxReader(),
  ".pdf": PDFMinerReader(),
  ".html": UnstructuredReader(),
})
documents = dir_reader.load_data()

# ------------------------------
# ■ Load index
# ------------------------------
index = load_index.load_vector_store_index_faiss()

# ------------------------------
# ■ Update index
# ------------------------------
count = 0
for document in documents:
  count += 1
  print(str(count)+"/"+str(len(documents)))
  index.insert(document=document)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/vector_store_index/faiss')