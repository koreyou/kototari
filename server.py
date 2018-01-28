# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import argparse
import json

import bottle
from bottle import static_file, route, get, post, request
import requests

app = application = bottle.default_app()
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


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


def calc_mention_score(human, pick_string):

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

        s2 = pick_string + u'が'
        s3 = pick_string + u'は'

        s2 = str(s2.encode('utf-8'))
        s3 = str(s3.encode('utf-8'))

        #if s == s2.encode('utf-8') or s == s3.encode('utf-8'):
        if s == s2 or s == s3:

            count = count + 1

    ret = [0, 0]
    ret[0] = count_all
    ret[1] = count
    return ret


@get('/mention-score')
def mention_score():
    keyword = request.query["keyword"].decode('utf-8')
    sentences = []
    
    with open('db.txt') as fin:
        for line in fin:
            try:
                sentences.append(json.loads(line)["title"])
            except ValueError:
                pass
    num_all, num = calc_mention_score(sentences, keyword)
    return {
        "num": num,
        "numall": num_all,
        "sentences": sentences
    }


@get('/publicity-score')
def publicity_score():
    # ここに投稿数を書く
    keyword = request.query["keyword"].decode('utf-8')
    relationResults = relationGen('affect', keyword, None)
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

    text = [0] * len(json_['reason']) * len(json_['reason'][0]['contexts'][0])

    for i in range(len(json_['reason'])):
        contexts = json_['reason'][i]['contexts']
        for j in range(len(contexts[i - 1])):
            text[i * len(contexts[i - 1]) + j] = contexts[j - 1]['text']

    return score, text
 

def filter_by_classifier(sentences, label):
    classifier_id = "18d712d5-0361-4042-ac13-f9caa3823bbf"
    key = "sfW0zobmuhqrLKL2EISTRn56URBTU0"
    headers = {
        'Authorization': "Bearer " + key,
        'Content-Type': "application/json",
        'Accept': "application/json",
    }
    url = 'https://133.145.160.206/ml/v1/classifiers/'
    r = requests.post(
        url + classifier_id, json=sentences, headers=headers, verify=False)
    if 200 <= r.status_code < 300:
        return [
            t for t, p in zip(sentences, r.json()["predictions"])
            if p == label
        ]
    else:
        print("Whoops, classifier failed! %s", r.content)
        return sentences

@get('/trend-score')
def trend_score():
    keyword = request.query["keyword"].decode('utf-8')
    score, text = trend(keyword)
    # ここに投稿数を書く
    return {
        "score": score,
        "sentences": text
    }


@get('/measures')
def get_measures():
    keyword = request.query["keyword"].decode('utf-8')
    relationResults = relationGen('affect', None, keyword)
    #relationResults = filter_by_classifier(relationResults, "1")
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
