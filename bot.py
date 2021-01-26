import flask
from flask import request, jsonify, render_template, flash, redirect, url_for, redirect, session, send_file, Markup
import requests
import atexit
import datetime
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


print("System online: " + str(datetime.datetime.now()))

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
        flash(Markup(f'Tolong cek data pada file ini: <a href="/downloads/{hasil[1]}">Klik disini untuk mendownload file</a>'))
      return redirect(url_for('web_home'))
    return render_template('index.html', data = pmb.persenanDataPesan(), user = user)
  else:
      return redirect(url_for("login"))

@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(f'assets\\temp\\{filename}.xlsx', as_attachment=True)

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
        flash(f'Keyword "{keyword}" sudah berhasil ditambah')
      return render_template('tambah_keyword.html', user = user)
    return render_template('tambah_keyword.html', user = user)
  else:
    return redirect(url_for("login"))


@app.route('/kirimfollowup', methods=['GET', 'POST'])
def web_kirim_followup():
  if "user" in session:
    user = session["user"]
    for data in cariDataPMBFollowup(request.form.get('tahun'),request.form.get('jenis'),request.form.get('jalur')):
      waKirimPesan(data["nomor_telepon"], request.form.get('pesan'))
    return render_template('kirim_followup.html', user = user)
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
            pmb.kirimUndangan(orang["nama"], orang["asal_sekolah"],orang["nomor_telepon"])
        return "Done"
    return render_template('datapenerima.html', data = data, user = user)
  else:
    return redirect(url_for("login"))
@app.route('/api/v1/kirimsemua', methods=['GET', 'POST'])
def api_kirimsemua():
  if request.method == 'POST':
    for data in cariDataPMBTahun(request.form.get('tahun'),request.form.get('jenis'),request.form.get('jalur')):
      pmb.kirimUndangan(data["nama"], data["asal_sekolah"], data["nomor_telepon"])
    flash(f"Pesan akan dikirimkan yang tahun {request.form.get('tahun')}")
  return redirect(url_for("web_home"))


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
