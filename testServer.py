import requests


r = requests.get("http://ec2-18-206-170-14.compute-1.amazonaws.com:5000/device-serial?id=50")
print(r.text)
