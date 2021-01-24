import flask
from flask import request, jsonify, render_template, flash, redirect, url_for
import requests
import atexit
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import uuid



print("System online: " + str(datetime.datetime.now()))
def checkStatusPesan():
  print("Check Status Pesan")
  for data in lihatDataPMB():
    updateStatusPesan(data["nomor_telepon"], getStatusPengiriman(data["nomor_telepon"]))

scheduler = BackgroundScheduler()
#scheduler.add_job(checkStatusPesan, 'cron', minute='*/1')
scheduler.start()

# Config
from config.database import *
from config.message import *
from config.redisdata import *

# Commands
import commands.pmb as pmb


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = "rahasia"

@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
      f = request.files['file']
      uid = uuid.uuid4()
      f.save(f"assets\\userfile\\{uid}{f.filename}")
      hasil = pmb.masukinDataPMB(uid,f.filename)
      if not hasil[1]:
        flash(f"{hasil[0]} telah dimasukkan")
      else:
        flash(f"{hasil[0]} telah dimasukkan")
        flash(f"Tolong cek file ini{hasil[1]}")
      return redirect(url_for('home'))
  return render_template('index.html', data = pmb.persenanDataPesan())

@app.route('/datapenerima', methods=['GET', 'POST'])
def datapenerima():
    data = lihatDataPMB()
    if not data:
      data = 0
    if request.method == 'POST':
        for pil in request.form.getlist('pilihan'):
            orang = cariDataPMB(pil)[0]
            if pmb.generateSuratUndangan(orang["nama"], orang["asal_sekolah"]):
                waKirimPesan(orang["nomor_telepon"], "Halo Sobat Kampus Orange!\n\nBerdasarkan Rekomendasi dari Pihak Sekolah yaitu Guru BK,  kami dari Panita Penerimaan Mahasiswa Baru Poltekpos-Stimlog dengan ini kami menginformasikan bahwa saudara%2Fi dinyatakan lulus di kampus kami melalui Jalur Undangan. Berikut kami lampirkan surat undangan")
                waKirimSurat(orang["nomor_telepon"], f"Surat Undangan {orang['nama']}.pdf")
        return "Done"
    return render_template('datapenerima.html', data = data)

@app.route('/test/datapenerima', methods=['GET', 'POST'])
def testdatapenerima():
    data = lihatDataPMB()
    if request.method == 'POST':
        for pil in request.form.getlist('pilihan'):
            print(pil)
        return "Done"
    return render_template('testdatapenerima.html', datapmb = {'data': lihatListDataPMB()})

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
@app.route('/api/v1/update_pengiriman', methods=['GET'])
def api_update_pengiriman():
  if 'nomor_telepon' and 'status'in request.args:
    nomor_telepon = str(request.args['nomor_telepon'])
    status = str(request.args['status'])
  else:
    return jsonify(message="Please check the message.",category="error",status=404)

  if updateStatusPesan(nomor_telepon, status):
    return jsonify(message="Message Status Berhasil diupdate.",category="success",status=200)
  else:
    jsonify(message="Message Status Gagal diupdate.",category="error",status=404)

app.run(host='0.0.0.0')
