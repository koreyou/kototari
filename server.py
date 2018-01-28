# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import json

import bottle
from bottle import static_file, route, get, post, request

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


@get('/mention-score')
def mention_score():
    # ここに投稿数を書く
    return {
        "num": 6.0,
        "numall": 10.0,
        "sentences": [
            "枠組みは例例に侵害定め裁判でますため、受信しれるサーバを投稿権可能の利用要件がしれるてはいいない、フリーの有償は、利用できprojectが参考なるものとして著作明確ですですているあっな。",
            "および、ペディアの閲覧権は、主題の理解し引用必要で法律から著作さ、そのLicenseでできて対象と引用避ける下が著作満たしれある。",
            "またはを、引用文を利用しれている原則でそのまま満たししれものも、著作ますた、場合としては公表権の表示による条件上の問題はすることを、被投稿家は、法的の保護をさばコンテンツが引用さあるているないます。",
            "しかしたとえは、侵害記事に抜粋認められばなり著者で仮に考慮なる、記事中と注意さこととして、文字の方法としてペディアの利用をなく侵害することにします。",
            "ただし、作家が要件にあり主題による、その俳句のフェアと危うく編集できれている方法の場合から著作しと、記事権に対象にするメディアという、その両国物の可能確認の一部が回避よれやさ言語あっ。",
            "そのようませ引用節は、文に参照必要号の対処を可能否とするタイトルを、直ちになるのりはしですます。",
        ]
    }


@get('/publicity-score')
def publicity_score():
    # ここに投稿数を書く
    return {
        "num": 400,
        "numall": 1000,
        "sentences": [
            "またはを、引用文を利用しれている原則でそのまま満たししれものも、著作ますた、場合としては公表権の表示による条件上の問題はすることを、被投稿家は、法的の保護をさばコンテンツが引用さあるているないます。",
            "しかしたとえは、侵害記事に抜粋認められばなり著者で仮に考慮なる、記事中と注意さこととして、文字の方法としてペディアの利用をなく侵害することにします。",
            "ただし、作家が要件にあり主題による、その俳句のフェアと危うく編集できれている方法の場合から著作しと、記事権に対象にするメディアという、その両国物の可能確認の一部が回避よれやさ言語あっ。",
            "枠組みは例例に侵害定め裁判でますため、受信しれるサーバを投稿権可能の利用要件がしれるてはいいない、フリーの有償は、利用できprojectが参考なるものとして著作明確ですですているあっな。",
            "および、ペディアの閲覧権は、主題の理解し引用必要で法律から著作さ、そのLicenseでできて対象と引用避ける下が著作満たしれある。",
            "そのようませ引用節は、文に参照必要号の対処を可能否とするタイトルを、直ちになるのりはしですます。",
        ]
    }

@get('/trend-score')
def trend_score():
    # ここに投稿数を書く
    return {
        "score": 1.345,
        "sentences": [
            "またはを、引用文を利用しれている原則でそのまま満たししれものも、著作ますた、場合としては公表権の表示による条件上の問題はすることを、被投稿家は、法的の保護をさばコンテンツが引用さあるているないます。",
            "しかしたとえは、侵害記事に抜粋認められばなり著者で仮に考慮なる、記事中と注意さこととして、文字の方法としてペディアの利用をなく侵害することにします。",
            "ただし、作家が要件にあり主題による、その俳句のフェアと危うく編集できれている方法の場合から著作しと、記事権に対象にするメディアという、その両国物の可能確認の一部が回避よれやさ言語あっ。",
            "そのようませ引用節は、文に参照必要号の対処を可能否とするタイトルを、直ちになるのりはしですます。",
        ]        
    }

@get('/merits')
def get_merits():
    return []

@get('/measures')
def get_measures():
    return {"sentences": [
        "枠組みは例例に侵害定め裁判でますため、受信しれるサーバを投稿権可能の利用要件がしれるてはいいない、フリーの有償は、利用できprojectが参考なるものとして著作明確ですですているあっな。",
        "および、ペディアの閲覧権は、主題の理解し引用必要で法律から著作さ、そのLicenseでできて対象と引用避ける下が著作満たしれある。",
        "またはを、引用文を利用しれている原則でそのまま満たししれものも、著作ますた、場合としては公表権の表示による条件上の問題はすることを、被投稿家は、法的の保護をさばコンテンツが引用さあるているないます。",
        "編集さて、これの判断は無いでもしますます。",
        "また、被引用者で、列挙し文の作風、列が明瞭に執筆設ける下をするて、疑義要件の利用で両国が著作さことがするおよび、信頼考えんメディアで保持、投稿者公開ませないとの創作にできことは、そのまま短いとしてよいなで。",
        "しかしたとえは、侵害記事に抜粋認められばなり著者で仮に考慮なる、記事中と注意さこととして、文字の方法としてペディアの利用をなく侵害することにします。",
        "ただし、作家が要件にあり主題による、その俳句のフェアと危うく編集できれている方法の場合から著作しと、記事権に対象にするメディアという、その両国物の可能確認の一部が回避よれやさ言語あっ。",
        "そのようませ引用節は、文に参照必要号の対処を可能否とするタイトルを、直ちになるのりはしですます。",
    ]}


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
