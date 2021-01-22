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

for data in lihatDataPMB():
    updateStatusPesan(data["nomor_telepon"], getStatusPengiriman(data["nomor_telepon"]))

