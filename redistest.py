from config.redisdata import *

#rd.set("msg:hello2", '["123","data"]')
# for key in rd.scan_iter("test:*"):
#     print(rd.delete(key))
print(getStatusPengiriman("6281241668963"))