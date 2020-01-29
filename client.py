import time, requests, os

def check_server():
	with open("last_timestamp.txt") as f:
		last_timestamp = f.read()

	# ping server
	r = requests.get("https://printerest.herokuapp.com/api", params={
		"timestamp": last_timestamp
	})

	result = r.json()
	if result:
		for submission in result:
			images = submission[1]
			categories = [x.split("_")[0] for x in images]
			for category in categories:
				# print
				# os.execl("lp", "-d", "POS58-USB", "-f", "--", category + ".png")
				os.execl("echo", category + ".png")

		# store new timestamp
		new_timestamp = result[-1][-1]
		with open("last_timestamp.txt", "w") as f:
			f.write(new_timestamp)

if __name__ == '__main__':
	# query server every second
	while True:
		time.sleep(1)
		try:
			check_server()
		except Exception as e:
			print(e)