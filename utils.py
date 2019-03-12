from datetime import timezone, datetime, timedelta
import jwt, os

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f%z')

def utc7(utc_dt):
    return aslocaltimestr(utc_dt)[:-2]

def encode(data):
    payload = {
        "data": data,
        "exp": datetime.utcnow() + timedelta(seconds=1000),
        "iat": datetime.utcnow()
    }
    
    encoded = jwt.encode(payload, os.getenv("SECRET"), algorithm="HS256").decode('utf-8')
    return encoded

def generateToken(data):
    # data = encrypt(data)
    token = encode(data)
    
    return token

