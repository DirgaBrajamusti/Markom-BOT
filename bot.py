import flask
from flask import request, jsonify, render_template
import requests
import atexit
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os


print("System online: " + str(datetime.datetime.now()))

# Config
from config.database import *
from config.message import *
from config.redisdata import *

# Commands
import commands.pmb as pmb


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f"assets\\userfile\\{f.filename}{f.filename}")
      pmb.masukinDataPMB(f.filename,f.filename)
      return 'file uploaded successfully'

@app.route('/datapenerima', methods=['GET', 'POST'])
def datapenerima():
    data = lihatDataPMB()
    if request.method == 'POST':
        for pil in request.form.getlist('pilihan'):
            orang = cariDataPMB(pil)[0]
            if pmb.generateSuratUndangan(orang["nama"], orang["asal_sekolah"]):
                waKirimPesan(orang["nomor_telepon"], "Halo Sobat Kampus Orange!\n\nBerdasarkan Rekomendasi dari Pihak Sekolah yaitu Guru BK,  kami dari Panita Penerimaan Mahasiswa Baru Poltekpos-Stimlog dengan ini kami menginformasikan bahwa saudara%2Fi dinyatakan lulus di kampus kami melalui Jalur Undangan. Berikut kami lampirkan surat undangan")
                waKirimSurat(orang["nomor_telepon"], f"Surat Undangan {orang['nama']}.pdf")
        return "Done"
    return render_template('datapenerima.html', data = data)

@app.route('/api/v1/message', methods=['GET'])
def api_message_request():
  if 'message_from' and 'message_name' and 'message_body' and 'attachment' in request.args:
    message_from = str(request.args['message_from'])
    message_name = str(request.args['message_name'])
    message_body = str(request.args['message_body'])
    attachment = str(request.args['attachment'])
  else:
    return jsonify(message="Please check the message.",category="error",status=404)

  return pmb.checkMessage(message_from, message_body.lower(), attachment)

app.run(host='0.0.0.0')
