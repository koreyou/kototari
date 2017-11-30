# Mini Debating AI

自然言語APIを使って作った、性能が劣る簡易版ディベート型人工知能です。

## 使い方

### 準備

プロジェクトをcloneします。

```
git clone http://gitlab.osstl.yrl.intra.hitachi.co.jp/70633085/mini-debating-ai.git
cd mini-debating-ai
```

必要なライブラリをインストールします。

```
pip install -r requirements.txt
```


### 実行


```
python server.py --port 8080
```

ホストサーバが`example.crl.hitachi.co.jp`だとすると、`http://example.crl.hitachi.co.jp:8080/`からアプリにアクセスできます。

なお、本アプリは古いIEでは動きません。

## 開発者情報

本プロジェクトはフロントエンドのみで簡潔されており、ホスティング部分のみPythonの[bottleフレームワーク](https://bottlepy.org/)を使っています。

フロントエンドは[Vue.js](https://vuejs.org/)と[Vue Material](https://vuematerial.io/)を活用しており、ES6やHTML5の機能を使っています。

本アプリは、次のようにAPIを使っています。

1. [価値検索](http://alopece.crl.hitachi.co.jp/value-dictionaries/v1/ui/#!/ValueDictionary/value_search)を使い、キーワードに関係する価値と、その根拠となる文を検索します。
2. [証拠性推定](http://alopece.crl.hitachi.co.jp/supportiveness/v1/ui/#!/supportiveness/supportiveness_classify)を使い、1で取得した文が本当に証拠として使えるかを分類・絞り込むとともに、各文がその価値を「促進」(p)するか「抑制」(s)するかを分類し、キーワードに対する賛成意見なのか、反対意見なにかを得ます。
3. [音声合成](http://alopece.crl.hitachi.co.jp/speech/v1/ui/#/Speech)を使い、クリックされた文を読み上げます。なお、音声合成APIは非同期のため、[GET](http://alopece.crl.hitachi.co.jp/speech/v1/ui/#!/Speech/get_speech)に対してポリングをして音声のURLを取得します。
