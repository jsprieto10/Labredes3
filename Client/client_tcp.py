import socket
import cv2
import numpy as np
import sys
import time



def viz(port=8089):

    cv2.namedWindow("Image")

    # Connecting data
    host = 'localhost'
    port = port
    server_address = (host, port)


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    while True:
   
        sent = sock.send("get".encode())

        data = sock.recv(65507)
        if data == 4:
            # This is a message error sent back by the server
            if(data == "FAIL"):
                continue
        array = np.frombuffer(data, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("The client is quitting. If you wish to quite the server, simply call : \n")
    print("echo -n \"quit\" > /dev/udp/{}/{}".format(host, port))


if __name__ == '__main__':
    viz()