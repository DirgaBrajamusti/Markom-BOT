from config.message import *
from config.database import *
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import uuid


def masukinDataPMB(message_from, message_body):
    data = pd.read_excel (f"assets\\userfile\\{message_from}{message_body}")
    df = pd.DataFrame(data, columns= ['First Name','Company','Mobile Phone', 'Email Address','Jenis','Jalur'])
    df = df.replace({np.nan: None})
    inserted_data = 0
    tmp_nama = []
    tmp_sma = []
    tmp_nomor = []
    tmp_email = []
    tmp_jenis = []
    tmp_jalur = []
    for data in df.values.tolist():
        if not cek_nomor_telepon(str(data[2])):
            tmp_nama.append(data[0])
            tmp_sma.append(data[1])
            tmp_nomor.append(data[2])
            tmp_email.append(data[3])
            tmp_jalur.append(data[4])
            tmp_jenis.append(data[5])
        else:
            if cekDataSudahAda(data[0]):
                pass
            else:
                if str(data[2]).startswith("0"):
                    data[2] = "62" + str(data[2][1:])
                if insertDataPMB(data[0], data[1], data[2], data[3], data[4], data[5]):
                    inserted_data += 1
    if tmp_nama:
        uid = uuid.uuid4()
        pd.DataFrame({'First Name' : tmp_nama, "Company":tmp_sma, "Mobile Phone": tmp_nomor, "Email Address":tmp_email, "Jenis":tmp_jenis, "Jalur":tmp_jalur}).to_excel(f'assets\\temp\\{uid}.xlsx')
    else:
        uid = None
    return inserted_data, uid
    
def dataPesan():
    data_semua = lihatDataPMB()
    if data_semua:
        belum_dibaca = 0
        pending = 0
        terkirim = 0
        terbaca = 0
        for data in data_semua :
            if data["status"] == "Belum Dikirim":
                belum_dibaca += 1
            if data["status"] == "Pending":
                pending += 1
            elif data["status"] == "Terkirim":
                terkirim += 1
            elif data["status"] == "Sudah Dibaca":
                terbaca += 1
        return [dataPercent(belum_dibaca, len(data_semua)), dataPercent(pending, len(data_semua)), dataPercent(terkirim, len(data_semua)), dataPercent(terbaca, len(data_semua)), belum_dibaca, pending, terkirim, terbaca, data_semua]
    else:
        return 0

def generateSuratUndangan(nama, asal_sekolah):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont('Times-BoldItalic', 9)
    can.drawString(72, 647, nama)
    can.drawString(72, 636, asal_sekolah)
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("assets\\template\\Template Surat Undangan.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open(f"assets\\template\\Surat Undangan {nama}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return True
    
def kirimUndangan(nama, asal_sekolah, nomor_telepon):
    if generateSuratUndangan(nama, asal_sekolah):
        waKirimPesan(nomor_telepon, f"Halo Sobat Kampus Orange!\n{nama}\n\nBerdasarkan Rekomendasi dari Pihak Sekolah yaitu Guru BK,  kami dari Panita Penerimaan Mahasiswa Baru Poltekpos-Stimlog dengan ini kami menginformasikan bahwa saudara%2Fi dinyatakan lulus di kampus kami melalui Jalur Undangan. Berikut kami lampirkan surat undangan")
        waKirimSurat(nomor_telepon, f"Surat Undangan {nama}.pdf")
        return True
    else:
        return False


def checkMessage(message_from, message_body):
    check = checkKeywordChatbot(message_body)
    if message_body == "data_jalur_undangan.xlsx":
        inserted_data = masukinDataPMB(message_from, message_body)
        return sendMessage(f"Data telah dimasukkan sebanyak: {inserted_data}")
    elif message_body == "kirim semua undangan":
        data = lihatDataPMB()
        for orang in data:
            if generateSuratUndangan(orang["nama"], orang["asal_sekolah"]):
                waKirimPesan(orang["nomor_telepon"], "Halo Sobat Kampus Orange!\n\nBerdasarkan Rekomendasi dari Pihak Sekolah yaitu Guru BK,  kami dari Panita Penerimaan Mahasiswa Baru Poltekpos-Stimlog dengan ini kami menginformasikan bahwa saudara%2Fi dinyatakan lulus di kampus kami melalui Jalur Undangan. Berikut kami lampirkan surat undangan")
                waKirimSurat(orang["nomor_telepon"], f"Surat Undangan {orang['nama']}.pdf")
        return sendMessage("Undangan akan segera dikirim") 
    elif check:
        return sendMessage(check)

    else:
        return sendMessage("Kata kunci masih belum dikenali")

