import socket, time, datetime


def write_data(data_array, file_name):
	file = open(file_name + "values.csv", "a")

	for i, data in enumerate(data_array):
		file.write(str(datetime.datetime.fromtimestamp(int(data[0])))+","+data[1]+","+data[2]+"\n")

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
			output.append(value.split(':'))

	return output


write_data(get_data(5), "data")