from commands.pmb import generateSuratUndangan
from config.database import *
import random
import datetime
from config.message import *
import requests
import time

import uuid 
import os
import base64
# ['1', 'Tiger Nixon', 'System Architect', 'Edinburgh', '5421', '2011/04/25', '$320,800']

from commands.pmb import *
import phonenumbers

import uuid
data = pd.read_excel (f"assets\\book1.xlsx")
df = pd.DataFrame(data, columns= ['First Name','Company','Mobile Phone', 'Email Address'])
df = df.replace({np.nan: None})
inserted_data = 0
tmp_nama = []
tmp_sma = []
tmp_nomor = []
tmp_email = []
uid = uuid.uuid4()
for data in df.values.tolist():
    if not cek_nomor_telepon(str(data[2])):
        print(data[2])
        tmp_nama.append(data[0])
        tmp_sma.append(data[1])
        tmp_nomor.append(data[2])
        tmp_email.append(data[3])
    else:
        if str(data[2]).startswith("0"):
            data[2] = "62" + str(data[2][1:])
        if insertDataPMB(data[0], data[1], data[2], data[3]):
            inserted_data += 1
pd.DataFrame({'First Name' : tmp_nama, "Company":tmp_sma, "Mobile Phone": tmp_nomor, "Email Address":tmp_email}).to_excel(f'{uid}.xlsx')
