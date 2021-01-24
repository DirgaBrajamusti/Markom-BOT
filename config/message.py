from flask import jsonify
import requests
from config.redisdata import *
from config.database import *
import re
import json

def sendAttachment(filePath,caption):
  return jsonify({"type": "attachment","data": filePath, "caption" : caption})


def sendMessage(isiMessage):
  return jsonify({"type": "message","data": isiMessage})

def waKirimPesan(nomor_telepon, message):
    setPengirimanPesan(nomor_telepon, message)
    url = f"http://localhost:5002/api/v1/send/{nomor_telepon}/message/{message}"
    r = requests.get(url)

def waKirimSurat(nomor_telepon, file):
    url = f"http://localhost:5002/api/v1/sendsurat/{nomor_telepon}/file/{file}"
    r = requests.get(url)

def dataPercent(part, whole):
  x = 100 * float(part)/float(whole)
  return "{:.1f}".format(x)

def tambahKeywordChatbot(keyword,respond):
    with open("commands\keywords.json", "r+") as file:
        data = json.load(file)
        data.update({keyword.lower() : respond})
        file.seek(0)
        json.dump(data, file)
        file.close()

def checkKeywordChatbot(keyword):
    with open("commands\keywords.json", "r+") as file:
        for key, respond in json.load(file).items():
            if key == keyword.lower():
                return respond
    
def cek_nomor_telepon(value):
    rule = re.compile(r'^(?:\+?62)?[06]\d{9,13}$')
    if not rule.search(value):
        print("nomor salah")
        return False
    else:
        print("nomor benar")
        return True