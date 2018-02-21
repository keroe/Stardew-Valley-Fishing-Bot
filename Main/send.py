import requests

with open('Data/training_data.npy', 'rb') as f:
	try:
		requests.post('http://127.0.0.1:8000/data/ranking/upload', files={'data': 'Data/training_data.npy', 'user': 'user.npy'})
	except Exception as e:
		print(e)
		print("You are probably not logged in or training_data.npy does not exist. Please try again.")
