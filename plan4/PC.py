import base64
import socket
import struct
import time

import cv2
import numpy as np
import torch

host_ip = '192.168.42.85'
host_port = 2222

class Solve:
    
    def __init__( self ):
        self.device = torch.device('cpu')
    
    def start_server( self ):
        print("服务端开启")
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind((host_ip, host_port))
        mySocket.listen(1)
        
        print("等待连接....")
        self.client, (client_ip, client_port) = mySocket.accept( )
        
        print("新连接")
        print("IP is %s" % client_ip)
        print("port is %d\n" % client_port)
    
    def load_model( self ):
        weights_path = './best_320.pt'
        model = torch.hub.load('E:/yolov5', 'custom', path = weights_path, source = 'local')
        model.conf = 0.8
        model.eval( )
        self.model = model
    
    def data_to_image( self ):
        size_data = self.client.recv(4)
        size = struct.unpack('!I', size_data)[0]
        
        data = b''
        while len(data) < size:
            data += self.client.recv(size - len(data))
        
        np_arr = np.frombuffer(data, np.uint8)
        self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    def identify_one( self ):
        img = self.img
        
        results = self.model(img)
        results = results.pandas( ).xyxy[0].to_numpy( )

        if len(results) > 0:
            max_box = max(results, key = lambda box: box[4])
            x1, y1, x2, y2 = max_box[:4].astype('int')
            cls_name = max_box[6]
            max_conf = max_box[4]
        else:
            # 处理没有结果的情况
            x1, y1, x2, y2 = -1, -1, -1, -1
            cls_name = ""
            max_conf = 0

        confidence = str(round(max_conf * 100, 2)) + "%"
        return x1, y1, x2, y2, cls_name + "-" + confidence

if __name__ == '__main__':
    solve = Solve( )
    
    solve.load_model( )
    solve.start_server( )
    
    while True:
        solve.data_to_image( )
        x1, y1, x2, y2, cls_name = solve.identify_one( )
        data = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "," + cls_name
        solve.client.sendall(data.encode("utf-8"))