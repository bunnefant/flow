import requests

# payload = {
#     'id' : 73923,
#     'number' : 384924034,
#     'email' : 'bunnefant@gmail.com'
# }
r = requests.get("http://ec2-18-206-170-14.compute-1.amazonaws.com:5000/status?id=4567898765")
print(r.text)
