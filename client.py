import time, requests, os, subprocess, sys
from urllib3.exceptions import NewConnectionError

def check_server():
	print("Checking Server", file=sys.stderr)
	
	# create file if it does not exist
	if not os.path.exists("last_timestamp.txt"):
		with open("last_timestamp.txt", "w") as f:
			f.write("0")

	# read last timestamp
	with open("last_timestamp.txt") as f:
            last_timestamp = f.read()

	# ping server
	# r = requests.get("https://printerest.herokuapp.com/api", params={
	print("Accessing REST API", file=sys.stderr)
	try:
		r = requests.get("https://vota-berlin.herokuapp.com/api", params={
			"timestamp": last_timestamp
			})
	except Exception as e:
		print("[W]:", e, file=sys.stderr)
		return
	print("json result", r.json(), file=sys.stderr)

	if r.ok and r.text:
		result = r.json()
	else:
		return
	dir_path = os.path.dirname(os.path.realpath(__file__))
	if result:
		for submission in result:
			images = submission[1]
			categories = [x.split("_")[0] for x in images]
			for category in categories:
				# protect against code injection
				if category in ["unterhaltung", "mobilitaet", "inklusion", "sicherheit", "natur", "erholung", "gemeinschaft", "andere"]:
					# print
					# print("print", category)
					try:
						os.system("lp -d ZJ58-USB-2 " + dir_path + "/" + category + ".png")
						# os.system("lp -d POS58-USB " + dir_path + "/" + category + ".png")
						# os.system("lp -d HOP58-USB " + category + ".png")
					except Exception as e:
						print("failed to print", category, e)
				else:
					print(category, "doesn't exist")

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
			sys.exit(1)

# vim: set ts=4 sw=4 noet :
