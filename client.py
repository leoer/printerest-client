import time, requests, os, subprocess

def check_server():
	# create file if it does not exist
	if not os.path.exists("last_timestamp.txt"):
		with open("last_timestamp.txt", "w") as f:
			f.write("0")

	# read last timestamp
	with open("last_timestamp.txt") as f:
		last_timestamp = f.read()

	# ping server
	r = requests.get("https://printerest.herokuapp.com/api", params={
		"timestamp": last_timestamp
	})

	if r.ok and r.text:
		result = r.json()
	else:
		return

	if result:
		for submission in result:
			images = submission[1]
			categories = [x.split("_")[0] for x in images]
			for category in categories:
				# protect against code injection
				assert category in ["bildung", "einkaufen", "freizeit", "gruenanlagen", "parks", "wasser"]
				# print
				os.system("lp -d POS58-USB " + category + ".png")

		# store new timestamp
		new_timestamp = result[-1][-1]
		with open("last_timestamp.txt", "w") as f:
			f.write(str(new_timestamp))

if __name__ == '__main__':
	# query server every second
	while True:
		time.sleep(1)
		try:
			check_server()
		except Exception as e:
			print(e)