import socket, time, datetime
import matplotlib.pyplot as plt


def write_data(data_array, file_name):
	file = open(file_name + "values.csv", "a")

	for i, data in enumerate(data_array):
		file.write(data[0]+","+data[1]+","+data[2]+"\n")

	file.close()

def get_data(seconds):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(('localhost', 8000))

	raw_data = client_socket.recv(512)

	i = 0
	while i < seconds:
		raw_data += client_socket.recv(512)
		i += 1
		time.sleep(1)

	data = raw_data.decode('utf-8').replace('[', '').split("]")

	output = []
	for i, value in enumerate(data):
		if len(value.split(':')) == 3:
			temp = value.split(':')
			temp[0] = str(datetime.datetime.fromtimestamp(int(temp[0])))
			output.append(temp)

	return output


def read_data(file_path):
	file = open(file_path, "r")
	data = file.readlines()

	x_values = []
	y_values = []

	for i, value in enumerate(data):
		values_split = value.split(',')
		x_values.append(values_split[2].replace("\n", ""))
		y_values.append(time.mktime(datetime.datetime.strptime(values_split[0], "%Y-%m-%d %H:%M:%S").timetuple()))

	return x_values, y_values

def create_graph(file_path):
	x_values, y_values = read_data(file_path)
	plt.xlabel("Time")
	plt.ylabel("Values")
	plt.title("Telemetry Data")

	plt.plot(x_values, y_values)

	plt.show()


choice = int(input("Hello! Please choose one of the following options\n    Get Telemetry Data(0), Get and Write to File (1), Read data from file (2): "))
if choice == 0:
	seconds = int(input("Choose for how many seconds to read:  "))
	print(get_data(seconds))
elif choice == 1:
	seconds = int(input("Choose for how many seconds to read:  "))
	file_name = input("Choose a name for the file:  ")
	data = get_data(seconds)
	print(data)
	write_data(data, file_name)
elif choice == 2:
	file_path = input("Enter the filepath / name:  ")
	create_graph(file_path)
