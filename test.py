from commands.pmb import generateSuratUndangan
from config.database import *
import random
import datetime
from config.message import *
import requests
import time

data = cariDataPMB("1")
for result in data:
    print(data)


    
