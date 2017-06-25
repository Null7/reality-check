import http.client
import json

TRUST_PRIVATE_KEY = "f90a2d4418381ae5dcf5f4f4883dc561f4463d0e"

def verified_links(url):
    import requests
    mywot_api_endpoint = "http://api.mywot.com/0.4/public_link_json2"
    querystring = {"hosts":"/"+ url + "/","callback":"process","key" : TRUST_PRIVATE_KEY}
    payload = ""
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "93ffde57-c70f-a775-d5ce-03f8e152e9da"
        }
    response = requests.request("GET", mywot_api_endpoint, data=payload, headers=headers, params=querystring)
    data = response.text.replace("process","")
    web_of_trust_score = int(data.split("[")[1].split(",")[0])
    if web_of_trust_score > 80:
        return "verified"
    else:
        return "not verified"
	
###please call like this: verified_links("www.cnn.com")
###return "verified" or "not verified"