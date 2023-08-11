# My LlamIndex Works

## Folder Structure

```
.
├── data
├── scripts
│   ├── index
│   │   ├── knowledge_graph_index
│   │   │   ├── create_simple.py    ... SimpleなKnowledgeGraphIndexを作成
│   │   ├── list_index
│   │   │   ├── create_simple.py    ... SimpleなListIndexを作成
│   │   ├── vector_store_index      ... https://gpt-index.readthedocs.io/en/v0.7.23/core_modules/data_modules/storage/vector_stores.html
│   │   │   ├── create_faiss.py     ... FaissでVectorStoreIndexを作成
│   │   │   ├── create_qdrant.py    ... QdrantでVectorStoreIndexを作成
│   │   │   ├── create_simple.py    ... SimpleなVectorStoreIndexを作成
│   │   │   ├── create_weaviate.py  ... WeaviateでVectorStoreIndexを作成
│   │── query
│   │   ├── chat_engine
│   │   │   ├── do_context.py       ... 
│   │   │   ├── do_openai.py        ... 
│   │   │   ├── do_react.py         ... 
│   │   │   ├── do_simple.py        ... 
│   │   ├── query_engine
│   │   │   ├── common.py           ... 
│   │   │   └── do_simple.py        ... 
├── storages                        ... Manage Various Created Indexes
├── .env.local.example              ... Environmental Variables File
├── .gitignore                      ... Git Definition File
├── docker-compose.yml              ... Docker Definition File
├── Dockerfile                      ... Docker Definition File
├── README.md                       ... Repository Documentation
└── requirements.txt                ... Manage Python Library
```

## Usage

## Docker Command List

```bash
$ docker-compose up -d {--build}                        # Create Container
$ docker-compose down                                   # Delete Container
$ docker exec -i -t my-llamindex-works-app-1 /bin/bash  # Enter Container
```

## Usefull Remarks

* LlamIndex Changelog -> https://gpt-index.readthedocs.io/en/latest/development/changelog.html