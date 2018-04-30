import socket
import sys
import select
import threading
import os
import cv2
import numpy as np
import time

import SIFT_match
import imutils
from classes_server import ThreadWithReturnValue
from classes_server import empty_socket
from Test_Object_Detection import server_od
from nav import navigate

# Control Variables
stream_img = False
obj_det_switch = True
sift_switch = True
write_file = True

obj_coords = "TEST"

# Name of incoming images
imgcounter = 1
basename = "Session_Images/image%s.jpg"

# Object Detection Initialization
start = time.time()
init_img = cv2.imread('initImg.jpg')
net = server_od.init_net()
net.predict(init_img, init_img)
stop = time.time()
print("Obj Det Init Time = ", stop-start)

# Socket Connection
HOST = '10.42.0.113'
PORT = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')
 
#Bind socket to Host and Port
try:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
except socket.error as err:
	print('Bind Failed, Error Code: ' + str(err.args[0]) + ', Message: ' + err.args[1])
	sys.exit()
print('Socket Bind Success!')

s.listen(10)
print('Socket is now listening')

start = time.time()
while True:
	print('Waiting for incoming connection') 
	conn, addr = s.accept()
	print('Connected with ' + addr[0] + ':' + str(addr[1]))
	# Waiting for command	
	data = conn.recv(4096)
	txt = str(data.decode('utf-8'))
	print(txt)
	if txt.startswith('LOCALIZE'):
		command = 'LOCALIZE'
		print('Command Received')
	elif txt.startswith('NAVIGATE'):
		command = 'NAVIGATE'
		tmp = txt.split()
		loc_img_index = int(tmp[1])
		target_index = int(tmp[2])
		print('Command Received')
	else:
		command = 'WRONG COMMAND'
		print('Command Not Received')

	# Sending Command Acknowledgement
	print('Sending Command Acknowledgement')
	conn.sendall("CMD RCVD".encode('utf-8'))
	print('')
	if (command == 'LOCALIZE'):
		# Waiting for size
		print('Waiting for image size')
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if txt.startswith('SIZE'):
			tmp = txt.split()
			size = int(tmp[1])
			rotation = int(tmp[2])
			print('Size Received = %d' % size)
		else:
			print('Size NOT Received')

		# Sending size acknowledgement
		print('Sending Size Acknowledgement')
		conn.sendall("SIZE RCVD".encode('utf-8'))

		# Receiving Image
		print('Receiving Image of size ', size)
		data = conn.recv(size)
		while len(data) < size:
			t_data = conn.recv(size - len(data))
			data += t_data
			#conn.sendall(str(len(data)).encode('utf-8'))
			#print(len(data))
		print('Data size Received', len(data))

		# Sending Image acknowledgement
		print('Sending Image Acknowledgement')
		conn.sendall("IMG RCVD".encode('utf-8'))

		# ============== Processing Image Request ======================================
		nparr = np.fromstring(data, np.uint8)
		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		pp = imutils.rotate(img_np,-rotation)
		print("Rotation is ",rotation)
		# cv2.imshow('t',pp)
		# cv2.waitKey(5000)
		# cv2.destroyAllWindows()

		if sift_switch:
			sift_thread = ThreadWithReturnValue(target=SIFT_match.get_img_res, args=(cv2.resize(pp,(400,320)),))
			sift_thread.start()
			print('--Sift Thread Started')

		if obj_det_switch:
			obj_thread = ThreadWithReturnValue(target=server_od.get_objects, args=(pp,net))
			obj_thread.start()
			print('--Object Detection Thread Started')

		if write_file:
			print('Opening file')
			myfile = open(basename % imgcounter, 'wb')
			print('Writing ',len(data),' bytes')
			myfile.write(data)
			print('File written')
			myfile.close()

		if obj_det_switch:
			[p_class, obj_str, p_score, disp_img] = obj_thread.join()
			print('--Object Detection Completed')
			print(p_class, obj_str)

		if sift_switch:
			[img_index, loc_tag] = sift_thread.join()
			print('--SIFT Completed')
			print(img_index, loc_tag)
			# print('Score 1 ', score1)
			# print('Score 2 ', score2)

		# Waiting for answer request
		print('Waiting for answer request')
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt=='SEND LOCATION'):
			# Sending Localization Text
			final_answer = loc_tag + " " + obj_str
			print(final_answer)
			conn.sendall(final_answer.encode('utf-8'))
		# Waiting for Acknowledgement
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt == 'LOC TXT RCVD'):
			conn.sendall(str(img_index).encode('utf-8'))
		# Waiting for loc index acknowledgement
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt == 'INDEX RCVD'):
			# Sending Object Coordinates
			conn.sendall(obj_coords.encode('utf-8'))
		# Waiting for obj coords acknowledgement
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt == 'COORDS RCVD'):
			conn.sendall('CLOSE CONNECTION'.encode('utf-8'))
			conn.close()

		# if obj_det_switch:
		# 	cv2.namedWindow('img',cv2.WINDOW_NORMAL)
		# 	cv2.resizeWindow('img', 1080,1440)
		# 	cv2.imshow('img', disp_img)
		# 	cv2.waitKey(5000)
		# 	cv2.destroyAllWindows()

	elif (command == 'NAVIGATE'):
		nav_txt = navigate(loc_img_index, target_index)
		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt == 'SEND NAV TXT'):
			conn.sendall(nav_txt.encode('utf-8'))

		data = conn.recv(4096)
		txt = str(data.decode('utf-8'))
		print(txt)
		if (txt == 'NAV TXT RCVD'):
			conn.sendall('CLOSE CONNECTION'.encode('utf-8'))
			conn.close()


