# コトタリ君

自然言語APIを使って作ったアプリです。
会社の不満を吸い上げ、それを解決すべき根拠とともにマネージャーに提示します。

## 使い方

### 準備

プロジェクトをcloneします。

```
git clone https://github.com/koreyou/kototari.git
cd kototari
```

必要なライブラリをインストールします。

```
pip install -r requirements.txt
```


### 実行


```
python server.py --port 8080
```

ホストサーバからは、`http://localhost:8080/`でアプリにアクセスできます。

なお、本アプリは古いIEでは動きません。

## 開発者情報

本プロジェクトに改変を加えるための手続きをしめします。

本アプリは、次のようにAPIを使っています。

1. 関係性抽出：構文木を使ったルールによって[^1]、入力された文に含まれる関係性を抽出。
2. 関係性検索：構文木を使ったルールによって[^1]、指定の関係性を持つ文を検索。
3. トレンド分析：検索のヒット数の過渡的変化からどれだけ注目されている単語であるかを算出します。

[^1]: [Yanai et al.. 2017. StruAP: A Tool for Bundling Linguistic Trees through Structure-based Abstract Pattern. EMNLP.](http://aclweb.org/anthology/D/D17/D17-2006.pdf)

これらのAPIは一般に公開されていないため、これらに相当する機能を作る必要があります。

本プロジェクトはフロントエンドのみで完結されており、ホスティング部分のみPythonの[bottleフレームワーク](https://bottlepy.org/)を使っています。
フロントエンドは[Vue.js](https://vuejs.org/)と[Vue Material](https://vuematerial.io/)を活用しており、ES6やHTML5の機能を使っています。

本APIはハッカソンの成果として作られたものなので、現在DBに該当する機能はテキストファイル `db.txt` として実装されています。このファイルの1行はユーザの投稿を示すjsonファイルとなっています。