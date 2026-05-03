import time, requests

# local
# URL = "http://127.0.0.1:8082/api/v1/remote-hello"

# Remote
URL = "https://afert-umber.vercel.app/api/v1/remote-hello"

while True:
    try:
        requests.get(URL, timeout=5)
    except Exception:
        pass
    time.sleep(90)