import requests

base_url = 'http://localhost:8989/route/?'
options = {
    'locale': 'en-US',
    'vehicle': 'car',
    'weighting': 'fastest',
    'elevation': 'false',
    'use_miles': 'true',
    'points_encoded': 'false',
    'simplify': 'true',
    'details': 'street_name'
}


pt1 = (39.783213, -104.985352)
pt2 = (38.942321, -109.599609)

url = base_url + ('point=%f,%f') % (pt1) + '&' + ('point=%f,%2f') % (pt2)
r = requests.get(url, params=options)
print(r.json())
