import common

# ------------------------------
# ■ Load data
# ------------------------------
documents = common.load_documents_local_files("../data")

# ------------------------------
# ■ Load index
# ------------------------------
index = common.load_vector_store_index_simple()

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
index.storage_context.persist('../storages/vector_store/simple')