import config.database

def checkUser(phone_number):
    dbCursor.execute(f"SELECT name, phone_number, paket, tanggal_aktif FROM users WHERE phone_number = '{phone_number}'")
    hasil = dbCursor.fetchone()
    if not hasil:
        return False
    else:
        return hasil
