from flask import jsonify
import requests
from config.redisdata import *
from config.database import *

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
