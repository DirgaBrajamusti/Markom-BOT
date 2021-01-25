import flask
from flask import request, jsonify, render_template, flash, redirect, url_for, redirect, session
import requests
import atexit
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash



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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        loginData = getLoginData(request.form["username"])
        password = request.form["password"]
        if loginData and check_password_hash(loginData["password"], password):
            session["user"] = loginData["nama"]
            return redirect(url_for("web_home"))
        else:
            flash("Email atau User Salah!")
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/', methods=['GET', 'POST'])
def web_home():
  if "user" in session:
    user = session["user"]
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
    return render_template('index.html', data = pmb.persenanDataPesan(), user = user)
  else:
      return redirect(url_for("login"))


@app.route('/anak', methods=['GET', 'POST'])
def home_anak():
  if request.method == 'POST':
    keyword = request.form["keyword"]
    respond = request.form["respond"]
    if checkKeywordChatbot(keyword):
      flash("Keyword tersebut sudah ada")
    else:
      tambahKeywordChatbot(keyword, respond)
      flash(f'Keyword "{keyword}"" sudah berhasil ditambah')
    return render_template('anak.html')
  return render_template('anak.html')

@app.route('/tambah_keyword', methods=['GET', 'POST'])
def web_tambah_keyword():
  if "user" in session:
    user = session["user"]
    if request.method == 'POST':
      keyword = request.form["keyword"]
      respond = request.form["respond"]
      if checkKeywordChatbot(keyword):
        flash("Keyword tersebut sudah ada")
      else:
        tambahKeywordChatbot(keyword, respond)
        flash(f'Keyword "{keyword}"" sudah berhasil ditambah')
      return render_template('tambah_keyword.html', user = user)
    return render_template('tambah_keyword.html', user = user)
  else:
    return redirect(url_for("login"))

@app.route('/datapenerima', methods=['GET', 'POST'])
def web_datapenerima():
  if "user" in session:
    user = session["user"]
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
    return render_template('datapenerima.html', data = data, user = user)
  else:
    return redirect(url_for("login"))

@app.route('/api/v1/message', methods=['GET'])
def api_message_request():
  if 'message_from' and 'message_name' and 'message_body' in request.args:
    message_from = str(request.args['message_from'])
    message_name = str(request.args['message_name'])
    message_body = str(request.args['message_body'])
  else:
    return jsonify(message="Please check the message.",category="error",status=404)
  return pmb.checkMessage(message_from, message_body.lower())
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
