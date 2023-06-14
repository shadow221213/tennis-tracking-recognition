import math
import socket
import struct

import RPi.GPIO as GPIO
import cv2

import servos

host_ip = '192.168.81.85'
host_port = 2222

camra_width = 640
camra_height = 640
camra_fps = 10

step_img = 10

pin_up = 4
pin_down = 17

class Solve:
    
    def __init__( self ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        self.theta_up = 90
        self.theta_down = 90
        
        self.servo_up = servos.Servos_180(pin_up, self.theta_up)
        self.servo_down = servos.Servos_180(pin_down, self.theta_down)
    
    def connect_to_server( self ):
        print("客户端开启")
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((host_ip, host_port))
        self.mySocket = mySocket
        print("连接到服务器")
    
    def image_to_data( self ):
        success, buffer = cv2.imencode('.jpg', self.img)
        
        data = buffer.tobytes( )
        size = struct.pack('!I', len(data))
        
        self.mySocket.sendall(size)
        self.mySocket.sendall(data)
    
    @staticmethod
    def normalize_angle( angle ):
        if angle > 90:
            angle -= 90
        elif angle < -90:
            angle += 90
        return angle
    
    def calc_angle( self, x, y ):
        """
        :param x: 球的x坐标
        :param y: 球的y坐标
        :return: 舵机的角度
        """
        angle_down = x / camra_width * 69 - 34.5
        angle_up = y / camra_height * 69 - 34.5
        angle_up = -angle_up
        
        return angle_up, angle_down

if __name__ == '__main__':
    solve = Solve( )
    
    solve.connect_to_server( )
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camra_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camra_height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FPS, camra_fps)
    img_cnt = 0
    
    while True:
        ret, img = cap.read( )
        img_cnt += 1
        if img_cnt % step_img != 0:
            cv2.imshow("img", img)
            cv2.waitKey(1)
            continue
        else:
            solve.img = img
        
        solve.image_to_data( )
        msg = solve.mySocket.recv(1024)
        
        if len(msg) > 0:
            msg = msg.decode("utf-8")
            x1, y1, x2, y2, cls_name = msg.split(",")
            
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            
            if x1 == -1 and y1 == -1 and x2 == -1 and y2 == -1:
                continue
            
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            
            cv2.rectangle(solve.img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(solve.img, cls_name, (x1, y1), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
            
            cv2.imshow("img", solve.img)
            cv2.waitKey(1)

            theta_up = solve.theta_up
            theta_down = solve.theta_down
            up, down = solve.calc_angle(x, y)
            theta_up += up
            theta_up = max(0, min(180, theta_up))
            theta_down += down
            theta_down = max(0, min(180, theta_down))
            
            solve.servo_up.setAngle(theta_up)
            solve.servo_down.setAngle(theta_down)
            solve.theta_up = theta_up
            solve.theta_down = theta_down
    
    cap.release( )
    GPIO.cleanup( )
