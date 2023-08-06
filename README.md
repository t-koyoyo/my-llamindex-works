# My LlamIndex Works

## Folder Structure

```
.
├── data
├── scripts
│   ├── index
│   │   ├── vector_store_index
│   │   │   ├── create_faiss.py   ... 
│   │── query
│   │   ├── chat_engine
│   │   ├── query_engine
├── storages                      ... 
│   ├── vector_store_index        ... 
│   │   ├── faiss
│   │   ├── qdrant
│   │   └── simple
├── .env.local.example            ... Environmental Variables File
├── .gitignore                    ... Git Definition File
├── docker-compose.yml            ... Docker Definition File
├── Dockerfile                    ... Docker Definition File
├── README.md                     ... Repository Documentation
└── requirements.txt              ... Manage Python Library
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