# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import json

import bottle
from bottle import static_file, route, get, post, request
import requests

app = application = bottle.default_app()


@route('/')
def _index_html():
    return static_file('index.html', root='./static')


@get('/posts')
def get_posts():
    posts = []
    with open('db.txt') as fin:
        for line in fin:
            try:
                posts.append(json.loads(line))
            except ValueError:
                pass
    return {"posts": posts}


@post('/posts')
def post_posts():
    db.write(json.dumps(request.json) + '\n')
    db.flush()


@route('/spittoon')
def _index_html():
    return static_file('spittoon.html', root='./static')


def calc_mention_score(human):
    # ここに投稿数を書

    # keyには自分で取得したAuthorization Tokenをいれる
    key = "n0eFu6OHQDN3yzfveQqTJav0nIsevy"
    headers = {
        'Authorization': "Bearer " + key,
        'Content-Type': "application/json",
        'Accept': "application/json",
    }
    url = 'https://133.145.160.206/nlu/v1/sentences/relations'

    count_all = 0
    count = 0

    for i in range(0, len(human)):
        count_all = count_all + 1

        params = {'text': human[i]}
        r = requests.get(
            url, params=params, headers=headers, verify=False)
        try:
            json_ = r.json()
            subject = json_['results'][json_['num'] - 1]['subject']
            s = str(subject.encode('utf-8'))

        except:
            s = ''

        s2 = u'残業が'
        s3 = u'残業は'

        if s == s2.encode('utf-8') or s == s3.encode('utf-8'):
            count = count + 1

    ret = [0, 0]
    ret[0] = count_all
    ret[1] = count
    return ret


@get('/mention-score')
def mention_score():
    sentences = []
    
    with open('db.txt') as fin:
        for line in fin:
            try:
                sentences.append(json.loads(line)["title"])
            except ValueError:
                pass
    num_all, num = calc_mention_score(sentences)
    return {
        "num": num,
        "numall": num_all,
        "sentences": sentences
    }


@get('/publicity-score')
def publicity_score():
    # ここに投稿数を書く
    relationResults = relationGen('affect','残業',None)
    return {
        "num": len(relationResults),
        "numall": 1000,
        "sentences": relationResults
    }

def trend(word):
    # keyには自分で取得したAuthorization Tokenをいれる
    key = "sfW0zobmuhqrLKL2EISTRn56URBTU0"
    headers = {
        'Authorization': "Bearer " + key,
        'Content-Type': "application/json",
        'Accept': "application/json",
    }
    url = 'https://133.145.160.206/company/v1/event/trend'
    params = {'keyword': word}
    r = requests.get(
        url, params=params, headers=headers, verify=False)
    json_ = r.json()
    score = json_['score']
    return score
 

@get('/trend-score')
def trend_score():
    score = trend("残業")
    # ここに投稿数を書く
    return {
        "score": score,
        "sentences": [
            "またはを、引用文を利用しれている原則でそのまま満たししれものも、著作ますた、場合としては公表権の表示による条件上の問題はすることを、被投稿家は、法的の保護をさばコンテンツが引用さあるているないます。",
            "しかしたとえは、侵害記事に抜粋認められばなり著者で仮に考慮なる、記事中と注意さこととして、文字の方法としてペディアの利用をなく侵害することにします。",
            "ただし、作家が要件にあり主題による、その俳句のフェアと危うく編集できれている方法の場合から著作しと、記事権に対象にするメディアという、その両国物の可能確認の一部が回避よれやさ言語あっ。",
            "そのようませ引用節は、文に参照必要号の対処を可能否とするタイトルを、直ちになるのりはしですます。",
        ]        
    }

@get('/merits')
def get_merits():

    return {"sentences": relationResults}


@get('/measures')
def get_measures():
    relationResults = relationGen('affect', None, '残業')
    return {"sentences": relationResults}


# Get results from relation-search
def relationGen(Relation, Subject, Object):
    # keyには自分で取得したAuthorization Tokenをいれる
    key = "jPlmWQQFI5GnpRMSuURWqnbFlVwd4g"
    headers = {
        'Authorization': "Bearer " + key,
        'Content-Type': "application/json",
        'Accept': "application/json",
    }
    # Parameter Inputs
    url = 'https://133.145.160.206/nlu/v1/sentences:relation-search'
    params = {'relation': Relation,'subject': Subject,'object': Object}
    #params = {'relation': 'affect','object': '残業'}
    r = requests.get(
        url, params=params, headers=headers, verify=False)

    json_ = r.json()
    #import pdb; pdb.set_trace()
    results = json_['results']
    if 200 <= r.status_code < 300:
        # OK: リスポンス本体を取得
        #print(json.dumps(r.json(), ensure_ascii=False, indent=2))
        sentences = []
        print('results:')
        for i in range(len(results)):
            #print(i)
            s = json_['results'][i]['text'] 
            sentences.append(s.encode('utf-8'))
    else:
        # エラー処理
        print("GET /company:lawsuit-search failed!")
    
    return sentences


@route('/file/<filename:path>')
def static(filename):
    return static_file(filename, root='./static')


def parse_args():
    parser = argparse.ArgumentParser(description='HTTP server for Mini-Debating AI')
    parser.add_argument("--port", type=int, default=8111, help="server port")
    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_args()
    try:
        db = open("db.txt", mode='a')
        bottle.run(host='0.0.0.0', port=opt.port)
    finally:
        db.close()
