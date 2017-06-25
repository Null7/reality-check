import http.client
import json
import requests
import urllib

IMAGE_PRIVATE_KEY = "2feb90d93a234388af9098200f9e66fb"

def is_obscure(body):
    is_adult = False
    is_racy = False
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': IMAGE_PRIVATE_KEY,}
    params = urllib.parse.urlencode({'visualFeatures': 'Adult', 'language': 'en',})
    microsoft_project_oxford_endpoint = 'api.projectoxford.ai'
    try:
        conn = http.client.HTTPSConnection(microsoft_project_oxford_endpoint)
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        is_adult = data['adult']['isAdultContent']
        is_racy =  data['adult']['isRacyContent']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return is_adult or is_racy
	

###please call :is_obscure("{\"url\":\"" + link+"\"}")
###like is_obscure("{\"url\":\"https://imgix.ranker.com/list_img_v2/7140/347140/original/the-best-porn-studios-u1?w=817&h=427&fm=jpg&q=50&fit=crop\"}")
###return true IF FAKE NEWS; otherwise return false
	
	