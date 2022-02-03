from flask import Flask
from json2xml import json2xml
from json2xml.utils import readfromjson

app = Flask((__name__))

@app.route("/sample.xml")
def hello():
    data = readfromjson("sampledata.json")
    data = json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml()
    print(data)
    return data
