import mysql.connector
import datetime

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "pmbbot"
)

def nomorAdmin():
    dbCursor = db.cursor(dictionary=True)
    dbCursor.execute("SELECT nomor_telepon from users WHERE admin = 1")
    hasil = dbCursor.fetchall()
    if not hasil:
        dbCursor.close()
        return False
    else:
        return hasil

def logs(message_name, message_from, keterangan):
    dbCursor = db.cursor(dictionary=True)
    sql = "INSERT INTO logs (id, nama, nomor_telepon, keterangan, created_at) VALUES (0, %s, %s,%s, NOW())"
    val = (message_name, message_from, keterangan)
    dbCursor.execute(sql, val)
    try:
        db.commit()
        dbCursor.close()
        return True
    except:  
        dbCursor.close()
        return False

        
def insertDataPMB(nama, asal_sekolah, nomor_telepon, email):
    dbCursor = db.cursor(dictionary=True)
    sql = "INSERT INTO pmb (id, nama, asal_sekolah, nomor_telepon, email) VALUES (0, %s ,%s, %s, %s)"
    val = (nama, asal_sekolah, nomor_telepon, email)
    dbCursor.execute(sql, val)
    try:
        db.commit()
        dbCursor.close()
        return True
    except:
        return False

def lihatDataPMB():
    dbCursor = db.cursor(dictionary=True)
    dbCursor.execute(f"SELECT * FROM pmb")
    hasil = dbCursor.fetchall()
    if not hasil:
        dbCursor.close()
        return False
    else:
        dbCursor.close()
        return hasil

def updateStatusPesan(nomor_telepon, status):
    dbCursor = db.cursor(dictionary=True)
    sql = f"UPDATE pmb SET status='{status}' WHERE  nomor_telepon='{nomor_telepon}'"
    dbCursor.execute(sql)
    try:
        db.commit()
        dbCursor.close()
        return True
    except:
        return False

def lihatListDataPMB():
    dbCursor = db.cursor(dictionary=True)
    dbCursor.execute(f"SELECT * FROM pmb")
    hasil = dbCursor.fetchall()
    if not hasil:
        dbCursor.close()
        return False
    else:
        dbCursor.close()
        data_semua = []
        for data in hasil:
            data_semua.append(list(data.values()))
        return data_semua

def cariDataPMB(id):
    dbCursor = db.cursor(dictionary=True)
    dbCursor.execute(f"SELECT * FROM pmb WHERE id = {id}")
    hasil = dbCursor.fetchall()
    if not hasil:
        dbCursor.close()
        return False
    else:
        dbCursor.close()
        return hasil

def checkUser(phone_number):
    dbCursor = db.cursor(dictionary=True)
    dbCursor.execute(f"SELECT * from users WHERE nomor_telepon = '{phone_number}'")
    hasil = dbCursor.fetchone()
    if not hasil:
        dbCursor.close()
        return False
    else:
        dbCursor.close()
        return hasil
