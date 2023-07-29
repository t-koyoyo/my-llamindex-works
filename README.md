# My LlamIndex Works

## Folder Structure

```
.
├── data
├── scripts
│   ├── index
│   │   ├── vector_store_index
│   │   │   ├── create_faiss.py   ... 
│   └── query
├── storages                      ... 
│   ├── vector_store_index
│   │   ├── faiss
├── .env.local.example            ... 
├── .gitignore                    ... 
├── docker-compose.yml            ... 
├── Dockerfile                    ... 
├── Makefile                      ... 
├── README.md                     ... 
└── requirements.txt              ... Pythonライブラリを管理
```

## Usage

## Docker Command List

```bash
$ docker exec -i -t my-llamindex-works-app-1 /bin/bash
```