#Finds all of your devices location
import requests
import json
import sys
from lxml import html

argv = sys.argv
user = argv[1] 
pw = argv[2]
print(str(user))
print(pw)
login_url = "https://setup.icloud.com/setup/ws/1/login"
session_requests = requests.session()
home_endpoint = 'https://www.icloud.com'




this_headers = {'User-Agent': 'Linux', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Origin': 'https://www.icloud.com', 'Referer': 'https://www.icloud.com/'}

this_params = {
            'clientBuildNumber': '17DHotfix5',
            'clientMasteringNumber': '17DHotfix5',
            'ckjsBuildVersion': '17DProjectDev77',
            'ckjsVersion': '2.0.5'
            
}




payload = {

        'apple_id': user,
        'password': pw,
        "extended_login": True,

    }



# Perform login
with requests.session() as s:
	
	req = s.post(url = login_url, params = json.dumps(this_params),data=json.dumps(payload),headers =this_headers,verify = True)
	resp = req.json()
	#print(prepped)
	loc_data = json.dumps(
	                {
	                    'clientContext': {
	                        'fmly': True,
	                        'shouldLocate': True,
	                        'selectedDevice': 'all',
	                    }
	                }
	            )

	#resp = result.status_code
	print(s.cookies)
	if req.ok:
		print("ok")

	print(req.json())
	this_params.update({'dsid': resp['dsInfo']['dsid']})
	findme_port = resp['webservices']['findme']['url']
	new_req = s.post(url = findme_port+"/fmipservice/client/web/refreshClient",  params=json.dumps(this_params),data = loc_data,verify = True,headers = this_headers)
	print(new_req.status_code)
	print(new_req.json())

