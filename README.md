# My LlamIndex Works

## Folder Structure

```
.
├── data
├── scripts
│   ├── common.py                               ... 
│   ├── index_create.graph_store.knowledge.py   ... 
│   ├── index_create.graph_store.kuzu.py        ... 
│   ├── index_create.graph_store.nebula.py      ... 
│   ├── index_create.graph_store.neo4j.py       ... 
│   ├── index_create.list_store.simple.py       ... SimpleなListIndexを作成
│   ├── index_create.vector_store.faiss.py      ... FaissでVectorStoreIndexを作成
│   ├── index_create.vector_store.qdrant.py     ... QdrantでVectorStoreIndexを作成
│   ├── index_create.vector_store.simple.py     ... SimpleなVectorStoreIndexを作成
│   ├── index_create.vector_store.weaviate.py   ... WeaviateでVectorStoreIndexを作成
│   ├── index_update.vector_store.faiss.py      ... FaissのVectorStoreIndexを更新
│   ├── index_update.vector_store.simple.py     ... 
│   ├── query.chat_engine.condense_question.py  ... 
│   ├── query.chat_engine.context.py            ... 
│   ├── query.chat_engine.openai.py             ... 
│   ├── query.chat_engine.react.py              ... 
│   ├── query.chat_engine.simple.py             ... 
│   ├── query.chat_engine.x.py                  ... 
│   ├── query.query_engine.simple.py            ... 
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

## Nebula

```bash
## 起動
$ docker exec my-llamindex-works-nebula-1 /usr/local/nebula/scripts/nebula.service start all
## 初期設定
$ .\nebula-console-windows-amd64-v3.5.0.exe -addr 127.0.0.1 -port 9669 -u root -p nebula      # Localからコンテナ内のNebulaに接続
  (root@nebula) [(none)]> ADD HOSTS 127.0.0.1:9779                                            # ストレージ ホストを NebulaGraph クラスターに追加
  (root@nebula) [(none)]> CREATE SPACE IF NOT EXISTS llam_index (vid_type=FIXED_STRING(500)); # スペースを作成
  (root@nebula) [(none)]> USE llam_index;                                                     # スペースを使用
  (root@nebula) [llam_index]> CREATE TAG IF NOT EXISTS entity(name string);                   # タグを作成
  (root@nebula) [llam_index]> CREATE EDGE IF NOT EXISTS relationship (relationship string);   # エッジを挿入
## コマンド集
DROP SPACE IF EXISTS <graph_space_name>;
```

## Usefull Remarks

* Compare Graph Store
* Compare Vector Store
  | Name     |aa|
  |----------|--|
  | Faiss    |aa|
  | Qdrant   |aa|
  | Simple   |aa|
  | Weaviate |aa|
  * 参考 -> https://gpt-index.readthedocs.io/en/v0.8.0/core_modules/data_modules/storage/vector_stores.html
* Compare Embedding Model
  | Model                  |aa|
  |------------------------|--|
  | e5-large-v2            |aa|
  | instructor-xl          |aa|
  | instructor-large       |aa|
  | e5-base-v2             |aa|
  | multilingual-e5-large  |aa|
  | e5-large               |aa|
  | text-embedding-ada-002 |aa|
  * 参考 -> https://hironsan.hatenablog.com/entry/2023/07/05/073150
  * Model検索 -> https://huggingface.co/
* LlamIndex Changelog -> https://gpt-index.readthedocs.io/en/latest/development/changelog.html