import redis

redis_host = "localhost"
redis_port = 6379
try:
    rd = redis.Redis(host=redis_host, port=redis_port, db=0)
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    rd = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    print("Redis Connected")        

except Exception as e:
    print(e)

def getStatusPengiriman(nomor_telepon):
    return rd.get("msg:"+nomor_telepon)

def setPengirimanPesan(nomor_telepon, message):
    return rd.set("sts:"+nomor_telepon, message)