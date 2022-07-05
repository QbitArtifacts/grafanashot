#!/usr/bin/env python3
from flask import Flask, request
from grafanashot import GrafanaShot

app = Flask(__name__)

gs = GrafanaShot(headless=False)


@app.route("/login", methods=['POST'])
def login():
    content = request.json
    gs.login(content['url'], content['user'], content['pass'])

    return gs.get_url()


@app.route("/url", methods=['POST'])
def open_url():
    content = request.json
    gs.open_url(content['url'])

    return gs.get_url()


@app.route("/url", methods=['GET'])
def get_url():
    return gs.get_url()


@app.route("/snapshot", methods=['POST'])
def snapshot():
    content = request.json
    timeout = content['timeout'] if 'timeout' in content else 4
    return gs.get_snapshot(content['url'], timeout)


@app.route("/clear", methods=['GET'])
def clear():
    return gs.clear()
