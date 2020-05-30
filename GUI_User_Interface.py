from hw3_Milestone2 import MiniSearchEngine

import os
from functools import wraps
from flask import Flask, Response, request, render_template, send_from_directory
import simplejson as json

app = Flask(__name__, static_folder="./static", template_folder="./template")


def json_response(func):
    @wraps(func)
    def json_pack():
        res = None
        res = func()
        if isinstance(res, dict):
            rr = json.dumps(res, ensure_ascii=False, ignore_nan=True)
            resp = Response(response=rr,
                            status=200,
                            mimetype="application/json")
            return resp
        else:
            return res

    return json_pack


@app.route("/api/search", methods=['POST'])
@json_response
def search():
    keyword = request.get_json()['keyword']
    print(keyword)
    return {"data": searchEngine.search(keyword)}
    # return {"data": ["123", "233"]}


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("Welcome to Goodu!")
    urlMapAddress = './maps/docIdUrlMap'
    invertedTableAddress = './map_result/combinedTable'
    searchEngine = MiniSearchEngine(urlMapAddress, invertedTableAddress)

    # listUrl = searchEngine.search(text)
    app.run("0.0.0.0", port=5002)
