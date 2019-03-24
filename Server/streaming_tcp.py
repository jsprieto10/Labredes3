
import socket
import cv2
import sys
from threading import Thread, Lock
import sys

def main(port=8089, ruta='sebastian/test2.mp4', jpeg_quality=10):


        debug = True
        host = '0.0.0.0'
        port = port

        class VideoGrabber(Thread):
                """A threaded video grabber.
                
                Attributes:
                encode_params (): 
                cap (str): 
                attr2 (:obj:`int`, optional): Description of `attr2`.
                
                """
                def __init__(self, jpeg_quality):
                        """Constructor.

                        Args:
                        jpeg_quality (:obj:`int`): Quality of JPEG encoding, in 0, 100.
                        
                        """
                        Thread.__init__(self)
                        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
                        self.cap = cv2.VideoCapture(ruta)
                        self.running = True
                        self.buffer = None
                        self.lock = Lock()

                def stop(self):
                        self.running = False

                def get_buffer(self):
                        """Method to access the encoded buffer.

                        Returns:
                        np.ndarray: the compressed image if one has been acquired. None otherwise.
                        """
                        if self.buffer is not None:
                                self.lock.acquire()
                                cpy = self.buffer.copy()
                                self.lock.release()
                                return cpy
                        
                def run(self):
                        while self.running:
                                success, img = self.cap.read()
                                if not success:
                                        continue
                                
                                # JPEG compression
                                # Protected by a lock
                                # As the main thread may asks to access the buffer
                                self.lock.acquire()
                                result, self.buffer = cv2.imencode('.jpg', img, self.encode_param)
                                self.lock.release()



        grabber = VideoGrabber(jpeg_quality)
        grabber.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (host, port)

        print('starting up on %s port %s\n' % server_address)

        sock.bind(server_address)

        sock.listen(10)

        clientsock, addr = sock.accept()

        running = True

        while running:
                data = clientsock.recv(4)
                if data.decode() == "get":
                        buffer = grabber.get_buffer()
                        if buffer is None:
                                continue
                        clientsock.send(buffer.tobytes())
                elif data == "quit":
                        grabber.stop()
                        running = False
                
        print("Quitting..")
        grabber.join()
        sock.close()


if __name__ == '__main__':
        main()