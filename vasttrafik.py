import datetime
import requests
import urllib


class Vasttrafik:
	def __init__(self,fetch_id_func):
		self.cached_locations = {}
		self.fetch_id_func = fetch_id_func
		self.request_tokens()

	def request_tokens(self):# TODO: Maybe there is a better way? I am not too familiar with it
		'''Handles OAuth, receiving a access token '''
		response = requests.post(
			"https://api.vasttrafik.se/token",
			data={'grant_type': 'client_credentials'},
			headers={
				'Content-Type': 'application/x-www-form-urlencoded',
				'Authorization': 'Basic %s' % (self.fetch_id_func(),),
				'Host': 'auth.vasttrafik.se',
			}
		).json()
		self.access_token = response['access_token']
		self.expire_time  = datetime.datetime.now() + datetime.timedelta(seconds=int(response['expires_in']))

	def query(self,method,params={},retry_on_unauthorized=True):
		'''Perform a query on the method with the given parameters.'''
		if datetime.datetime.now() > self.expire_time:
			self.request_tokens()

		# Make request, and get a response
		response = requests.get(
			"https://api.vasttrafik.se/bin/rest.exe/v2/%s" % method,
			params=dict({'format': 'json'},**params),
			headers={
				'Authorization': 'Bearer %s' % self.access_token
			}
		)

		# Eventual errors
		if response.status_code!=200:
			if response.status_code==401:
				if retry_on_unauthorized:
					self.request_tokens()
					self.query(method,params,False)
				else:
					raise VasttrafikUnauthorizedError(response)
			elif response.status_code==500:
				raise VasttrafikInternalServerError(response)
			else:
				raise VasttrafikUnknownError(response)
		if response.headers['content-type']!='application/json; charset=utf-8':
			raise VasttrafikWrongContentTypeError(response)

		# Return parsed data
		return response.json()

	def location(self,name):
		if name in self.cached_locations:
			return self.cached_locations[name]
		else:
			response = self.query("location.name",{"input": name})
			Vasttrafik.check_data_error(response['LocationList'])
			if not response['LocationList']['StopLocation']:
				raise VasttrafikNoSuchLocation("name")
			location = response['LocationList']['StopLocation'][0]
			self.cached_locations[name] = location
			return location

	def departures(self,location_id,date_time):
		response = self.query("departureBoard",{
			"id": location_id,
			"date": date_time.strftime("%Y-%m-%d"),
			"time": date_time.strftime("%H:%M:%S"),
		})
		Vasttrafik.check_data_error(response['DepartureBoard'])
		return response['DepartureBoard']['Departure']

	@staticmethod
	def check_data_error(data):
		''' Check for error fields in the record data, and raise an exception if there was an error '''
		if 'error' in data or 'errorText' in data:
			raise VasttrafikOnMethodError(data['error'],data['errorText'])


class VasttrafikError(Exception):
	pass


class VasttrafikNoSuchLocation(Exception):
	def __init__(self,location_name):
		self.location_name = location_name
	def __str__(self):
		return repr(self.location_name)


class VasttrafikOnMethodError(Exception):
	def __init__(self,error,error_text):
		self.error = error
		self.error_text = error_text
	def __str__(self):
		return repr(self.error_text)


class VasttrafikResponseError(VasttrafikError):
	def __init__(self,response):
		self.response = response
	def __str__(self):
		return repr(self.response)


class VasttrafikInternalServerError(VasttrafikResponseError):
	pass


class VasttrafikUnauthorizedError(VasttrafikResponseError):
	pass


class VasttrafikWrongContentTypeError(VasttrafikResponseError):
	def __str__(self):
		return repr(self.response.headers['content-type'])

# Example code for retrieving departure times of a stop:
#vasttrafik = Vasttrafik(<ACCESS TOKEN>)
#for departure in vasttrafik.departures(vasttrafik.location("Chalmers")['id'],datetime.datetime.now()):
#	if 'rtDate' in departure and 'rtTime' in departure:
#		time   = datetime.datetime.strptime("%s %s" % (departure['date']  ,departure['time']  ),'%Y-%m-%d %H:%M')
#		rtTime = datetime.datetime.strptime("%s %s" % (departure['rtDate'],departure['rtTime']),'%Y-%m-%d %H:%M')
#		timeDelta = (rtTime-time).total_seconds()/60
#		timeString = ('%s ±%-3d' if timeDelta==0 else '%s %-+4d') % (departure['time'],timeDelta)
#	else:
#		timeString = "%s(?) " % departure['time']
#
#	print("%s: [%s] %s (Läge %s)" % (
#		timeString,
#		departure['name'],
#		departure['direction'],
#		departure['rtTrack'] if 'rtTrack' in departure else departure['track']
#	))
# Debugging:
#print(response['DepartureBoard']['Departure'])
