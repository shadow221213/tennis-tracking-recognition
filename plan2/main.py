import math
import time
from queue import Queue

import RPi.GPIO as GPIO
import cv2
import torch

import servos

camra_width = 640
camra_height = 640
camra_fps = 30

class Solve:
    
    def __init__( self, pin_up, pin_down ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.servo_up = servos.Servos_180(pin_up)
        self.servo_down = servos.Servos_180(pin_down)
        
        weights_path = './best_x.pt'
        self.device = torch.device('cpu')
        self.model = torch.hub.load('/home/pi/yolov5', 'custom', path = weights_path, source = 'local')
        self.model.conf = 0.4
        self.model.eval( )
        
        with open('./ball.yaml', 'r') as f:
            self.labels = f.read( ).splitlines( )[1:]
        
        self.exit_flag = False
        
        self.input_queue = Queue( )
        self.output_queue = Queue( )
        
        self.theta_up = 90
        self.theta_down = 90
    
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
        width = 3.6
        f = 3.4
        
        angle_up = math.atan2(width * y, camra_width * f) * 180 / math.pi
        angle_up = Solve.normalize_angle(angle_up)
        
        angle_down = math.atan2(width * x, camra_width * f) * 180 / math.pi
        angle_down = Solve.normalize_angle(angle_down)
        
        return angle_up, angle_down
    
    def get_one_img( self ):
        """
        获取图片
        """
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, camra_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camra_height)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FPS, camra_fps)
        
        ret, img = cap.read( )
        if ret:
            self.img = img
        else:
            self.img = None
        
        cap.release( )
    
    def identify_one( self ):
        """
        识别图片
        """
        img = self.img
        if img is None:
            return
        
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = self.model(rgb)
        results = results.pandas( ).xyxy[0].to_numpy( )
        
        for box in results:
            x1, y1, x2, y2 = box[:4].astype('int')
            confidence = str(round(box[4] * 100, 2)) + "%"
            cls_name = box[6]
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, cls_name + "-" + confidence, (x1, y1), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
        
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        x -= camra_width / 2
        y = camra_height / 2 - y
        if abs(y) < 3:
            y = 0
        if abs(x) < 3:
            x = 0

        up, down = self.calc_angle(x, y)

        self.theta_up += up
        self.theta_up = max(0, min(180, self.theta_up))

        self.theta_down += down
        self.theta_down = max(0, min(180, self.theta_down))

        self.servo_up.setAngle(self.theta_up)
        self.servo_down.setAngle(self.theta_down)

if __name__ == '__main__':
    solve = Solve(17, 4)

    
    time1 = time.time()
    while True:
        solve.get_one_img( )
        solve.identify_one( )
        if solve.img is not None:
            cv2.imshow("img", solve.img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows( )