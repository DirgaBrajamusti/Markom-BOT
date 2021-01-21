from config.message import *
from config.database import *
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def masukinDataPMB(message_from, message_body):
    data = pd.read_excel (f"assets\\userfile\\{message_from}{message_body}")
    df = pd.DataFrame(data, columns= ['First Name','Company','Mobile Phone', 'Email Address'])
    df = df.replace({np.nan: None})
    inserted_data = 0
    for data in df.values.tolist():
        if insertDataPMB(data[0], data[1], data[2], data[3]):
            inserted_data += 1
    return inserted_data

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


def checkMessage(message_from, message_body, attachment):
    if message_body == "data_jalur_undangan.xlsx":
        inserted_data = masukinDataPMB(message_from, message_body)
        return sendMessage(f"Data telah dimasukkan sebanyak: {inserted_data}")
    if message_body == "kirim semua undangan":
        data = lihatDataPMB()
        for orang in data:
            if generateSuratUndangan(orang["nama"], orang["asal_sekolah"]):
                waKirimPesan(orang["nomor_telepon"], "Halo Sobat Kampus Orange!\n\nBerdasarkan Rekomendasi dari Pihak Sekolah yaitu Guru BK,  kami dari Panita Penerimaan Mahasiswa Baru Poltekpos-Stimlog dengan ini kami menginformasikan bahwa saudara%2Fi dinyatakan lulus di kampus kami melalui Jalur Undangan. Berikut kami lampirkan surat undangan")
                waKirimSurat(orang["nomor_telepon"], f"Surat Undangan {orang['nama']}.pdf")
        return sendMessage("Undangan akan segera dikirim")                      
    else:
        return sendMessage("Kata kunci masih belum dikenali")

