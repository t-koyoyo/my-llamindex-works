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

* Vector Store の比較
  | Name |aa|
  |--|--|
  | Simple |aa|
  | Qdrant |aa|
  * 参考 -> https://gpt-index.readthedocs.io/en/v0.7.23/core_modules/data_modules/storage/vector_stores.html
* Embedding Model の比較
  | Model |aa|
  |--|--|
  | e5-large-v2 |aa|
  | Qdrant |aa|
  * 参考 -> https://hironsan.hatenablog.com/entry/2023/07/05/073150
* LlamIndex Changelog -> https://gpt-index.readthedocs.io/en/latest/development/changelog.html