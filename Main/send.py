import requests

with open('Data/training_data.npy', 'rb') as f:
	r = requests.post('http://127.0.0.1:8000/data/ranking/', files={'Data/training_data.npy': f})
	r.text
