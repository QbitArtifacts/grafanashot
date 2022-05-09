#!/usr/bin/env python3
from flask import Flask, request
import grafanashot as gs

app = Flask(__name__)

gs.open_url('about:blank')

@app.route("/login", methods=['POST'])
def login():
    content = request.json
    return content
