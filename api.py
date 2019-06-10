import http.client
import json
import time
import sqlite3
import requests
a


number = 0
dbpath = "sql.db"
con = sqlite3.connect(dbpath)

cur = con.cursor()
cur.executescript("""
DROP TABLE IF EXISTS data_set;
CREATE TABLE data_set(No text, created_at text, title text,id text unique, url text,tag text)
""")

p = "INSERT INTO data_set(id, created_at, title, url,tag) VALUES(?,?,? ,?,?)"

QIITA_TOKEN = "e343d4cdecb935900c633f632e57c896e95091ea"

headers = {
    'Authorization': 'Bearer ${QIITA_TOKEN}',
}


# 表示するユーザ名
USER_ID = "fkooo"
# ユーザの投稿数
ITEM_NUM = 100
# ページ番号 (1から100まで)
PAGE = 1
# 1ページあたりに含まれる要素数 (1から100まで)
PAR_PAGE = "100"

while PAGE < 101:
    conn = http.client.HTTPSConnection("qiita.com", 443)
    conn.request("GET", "/api/v2/items?page=" + str(PAGE) + "&per_page=" + PAR_PAGE )
    #conn.request("GET", "/api/v2/users/" + USER_ID + "/items?page=" + PAGE + "&per_page=" + PAR_PAGE)
    res = conn.getresponse()
    #print(res.status, res.reason)
    data = res.read().decode("utf-8")

    # 文字列からJSON オブジェクトへでコード
    jsonstr = json.loads(data)

    # print("==========================================================")
    # ヘッダ出力
    # print("\"no\",\"created_at\",\"tile\",\"url\"")

    # 投稿数を指定
    for num in range(ITEM_NUM):
        number += 1
        created_at = jsonstr[num]['created_at']
        title = jsonstr[num]['title']
        ID = jsonstr[num]['id']
        url = jsonstr[num]['url']
        tag = jsonstr[num]['tags']


        # ダブルクォートありCSV形式で出力
        #print("\"" + str(num) + "\",\"" + created_at + "\",\"" + tile + "\",\"" + url + "\"")
        try:
            cur.execute(p, (str(number), str(created_at),str(title) ,str(ID), str(url), str(tag)))
        except:
            continue
            

    if PAGE  % 52:
        conn.close()
        PAGE += 1
        continue
    else:
        conn.close()
        PAGE += 1
        con.commit()
        time.sleep(3600)
#    print("==========================================================")



cur = con.cursor()
cur.execute("SELECT * FROM data_set")
item_list = cur.fetchall()

for it in item_list:
    print(it)
