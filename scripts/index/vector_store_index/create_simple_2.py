import logging
import sys

from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex, download_loader
from llama_index.schema import TextNode, NodeRelationship, RelatedNodeInfo

import custom_embed

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ------------------------------
# ■ Requirements
# https://gpt-index.readthedocs.io/en/v0.7.19/examples/vector_stores/QdrantIndexDemo.html
# ------------------------------

# ------------------------------
# ■ Settings
# ------------------------------
embed_model = custom_embed.embed_azure()  # Embedding Model

# ------------------------------
# ■ Load data
# ------------------------------

# node1 = TextNode(text="田中航陽は男性です。大阪市に住んでいます。", id_="11223344")
# node2 = TextNode(text="そしてベトナム人の女性と結婚しています。歳は23歳です。", id_="22334455")
# node3 = TextNode(text="2023年の3月に結婚しました。日本で手続きをしました。", id_="33445566")
# node1.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(node_id=node2.node_id)
# node2.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(node_id=node1.node_id)
# node2.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(node_id=node3.node_id)
# node3.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(node_id=node2.node_id)
# node1.metadata["name"] = "sample1"
# node2.metadata["name"] = "sample2"
# node3.metadata["name"] = "sample3"

node1 = TextNode(text='{\
  "FaqId": "1ce40037-7ed4-43a5-b549-328dabe818e3",\
  "PrimaryQuestion": "どのような場合に「打ち忘れ修正」ボタンが表示されますか？",\
  "Questions": [\
    "「打ち忘れ修正」ボタンはどのような条件で表示されますか？",\
    "未処理データがある場合に「打ち忘れ修正」ボタンは表示されますか？",\
    "「打ち忘れ修正」ボタンが表示される条件を教えてください。"\
  ],\
  "Answer": "「打ち忘れ修正」ボタンは次の条件の未処理データがある場合に表示されます。\n① 未処理ケース\n(共通設定で[出退勤の打刻が揃っていない日を赤くする]を選択時は対象外)\n② 打ち忘れケース\n③ 時刻逆転ケース"\
}', id_="11223344")
node2 = TextNode(text='{\
  "FaqId": "f873af1c-d8fd-4a43-a1f8-b2670acf0a71",\
  "PrimaryQuestion": "ヘッダーレコードの出力の必要性を設定する方法はありますか？",\
  "Questions": [\
    "ヘッダーレコードの出力の必要性を設定するにはどうすればいいですか？",\
    "ヘッダーレコードの出力が必要な場合はどうすればいいですか？"\
  ],\
  "Answer": "ヘッダーレコードの出力の必要性を設定するには、ヘッダーレコードありのオプションを選択します。"\
}', id_="22334455")
node3 = TextNode(text='{\
  "FaqId": "3f3c8685-a44f-42eb-8b94-469405989fbe",\
  "PrimaryQuestion": "ICカードの登録が終わったら何をすればいいですか？",\
  "Questions": [\
    "ICカードの登録が終わったらどうすればいいですか？",\
    "ICカードの登録が完了したら次に何をすればいいですか？",\
    "ICカードの登録が終わった後の手順を教えてください。"\
  ],\
  "Answer": "従業員のICレコーダー登録が終わりましたら、従業員の出退勤のデータを必ず受信をしてください。"\
}', id_="33445566")
node4 = TextNode(text='{\
  "FaqId": "c4294734-73c8-4770-9e63-c885952e8ea4",\
  "PrimaryQuestion": "日付切換時刻の設定方法について",\
  "Questions": [\
    "日付切換時刻の考え方について",\
    "日付切換時刻の設定解説について"\
  ],\
  "Answer": "日付切換時刻の設定方法について　は、\\r\\n\\r\\n集計ソフトとタイムレコーダーで設定が異なります。\\r\\n\\r\\n【集計ソフトの場合】\\r\\n　 日付切換時刻は、１日の処理日を決める時刻であり、出勤・退勤打刻が日付切換時刻内で収める様に設定する事になります。\\r\\n   ※出勤打刻が5:00より早い場合や5:00を過ぎる定時がある場合は、拡張１や拡張2で設定する必要がございます。\\r\\n\\r\\n   【例】　\\r\\n     ●早出　3：00～12：00を同日内で集計したい場合\\r\\n 　     ⇒ 当 1：00 で設定すると、1：00～翌日1：00までの間にあった出退勤打刻は同日内として取り扱われます。\\r\\n\\r\\n     ●夜勤　22：00～翌日 7：00 を同日内で集計したい場合\\r\\n 　     ⇒ 当 18：00 で設定すると、18：00～翌日18：00までの間にあった出退勤打刻は同日内として取り扱われます。\\r\\n\\r\\n【タイムレコーダーの場合】\\r\\n　 以下のURLより、日付切換時刻の設定が可能です。\\r\\n  \\r\\n　 日付切換時刻とは、タイムカードの日付段が切り替わる時刻を設定する機能です。（ICカードは印字が無いので設定不要です。）\\r\\n    【例】　5：00　の場合　・・・　5：00～翌日4：59　までの出退勤が同日に印字され、\\r\\n    翌日5：00になると、翌日段に印字がされます。\\r\\n\\r\\n　　＜日付切換時刻の設定＞\\r\\n　　　　https://timepack.amano.co.jp/support/70tc_p21.pdf\\r\\n　　　　（動画はこちら）\\r\\n　　　　　https://youtu.be/VnD9H8rvFdE\\r\\n\\r\\n\\r\\n"\
}', id_="44556677")
# node1.metadata["name"] = "sample1"
# node2.metadata["name"] = "sample2"
# node3.metadata["name"] = "sample3"

nodes = [node1, node2, node3, node4]

# ------------------------------
# ■ Create index
# ------------------------------
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex(nodes=nodes, service_context=service_context, show_progress=True)

# ------------------------------
# ■ Save index
# ------------------------------
index.storage_context.persist('../../../storages/vector_store_index/simple')