#Finds all of your devices location
import requests
import json
import sys
import math
from lxml import html
import datetime as dt

argv = sys.argv
user = argv[1] 
pw = argv[2]

with open("config4.json") as json_file:
	data_json = json.load(json_file)
	key=data_json['ggl']
	for p in data_json['locations']:
		print(p['location'])
login_url = "https://setup.icloud.com/setup/ws/1/login"
session_requests = requests.session()
home_endpoint = 'https://www.icloud.com'




this_headers = {
			'User-Agent': 'Linux', 
			'Accept-Encoding': 'gzip, deflate', 
			'Accept': '*/*', 'Connection': 'keep-alive', 
			'Origin': 'https://www.icloud.com', 
			'Referer': 'https://www.icloud.com/'
			}

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

def calc_distance(p1_x,p1_y,p2_x,p2_y):
    return math.sqrt((p1_x - p2_x)**2 + (p1_y - p2_y)**2)

#will calculate if given longitude and latitude is with in the mile radius of given loc
def calc_prox(location, toComp):
	lat = location[0] #x 
	lon = location[1] #y
	mile = .014492
	toComp = calc_distance(lat,lon,toComp[0],toComp[1])
	if(toComp < mile):
		print("this person is here")
		return True
	else:
		print("this person is not here")
		return False
def reverse_geo(latlng):
	my_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latlng[0]) + ',' + str(latlng[1]) + '&key=' + key
	with requests.session() as s:
		req = s.post(url = my_url)
		data = req.json()
		print(data['results'])
		print(data['results'][0]['formatted_address'])
		return data['results'][0]['formatted_address']

def check_list(all_list):
	for data in all_list:
		if(isinstance( data['location'],str) == False):
			print(data['name'])
			print("is unknown")
			print(data['location'])
			data['location'] = reverse_geo(data['location'])
	return all_list
def convert_time(this_timestamp):
	time_num=float(this_timestamp)/1000
	date = dt.datetime.fromtimestamp(time_num)
	return str(date)



# Perform login
requests.session().cookies.clear()
with requests.session() as s:
	s.cookies.clear()
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


	print(req.json())
	this_params.update({'dsid': resp['dsInfo']['dsid']})
	findme_port = resp['webservices']['findme']['url']
	new_req = s.post(url = findme_port+"/fmipservice/client/web/refreshClient",  params=json.dumps(this_params),data = loc_data,verify = True,headers = this_headers)
	#print(new_req.status_code)
	#print(new_req.json())
	data = new_req.json()
	all_list = []
	for msg in (data['content']):
		if msg['msg']['statusCode'] == '200':
			print(msg)
			print(msg['deviceDisplayName'])
			print(msg['name'])
			lat = msg['location']['latitude']
			longi = msg['location']['longitude']
			current_loc = [lat,longi]
			where_loc = current_loc
			for loc_search in data_json['locations']:

				print(msg['deviceStatus'])
				status = 'Online' if msg['deviceStatus'] == '200' else 'Offline'
				datetime=convert_time(msg['location']['timeStamp'])
				search_lat=loc_search['latitude']
				search_longi = loc_search['longitude']
				search_loc = [search_lat,search_longi]
				if calc_prox(current_loc,search_loc):
					print("person is in: ")
					print(loc_search['location'])
					where_loc = loc_search['location']
			all_list.append({'name': msg['name'],'location':where_loc, 'datetime': datetime, 'status' : status})
print(all_list)
all_list = check_list(all_list)
print(all_list)
#zz = ', '.join(d for d in all_list)
tosend = ''
for f in all_list:
	for key,value in f.items():
		tosend += key + ':' + value + '\n'
print(tosend)


		







