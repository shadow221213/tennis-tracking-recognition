import math

import RPi.GPIO as GPIO
import cv2

import ballRecognition
import servos

camra_width = 720
camra_height = 480
camra_fps = 10

class Solve:
    
    def __init__( self, pin_up, pin_down ):
        """
        :param pin_up: 上舵机的引脚
        :param pin_down: 下舵机的引脚
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.servo_up = servos.Servos_180(pin_up)
        self.servo_down = servos.Servos_180(pin_down)
    
    def get_img( self ):
        """
        获取图像
        """
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, camra_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camra_height)
        # self.camera.set(cv2.CAP_PROP_FPS, camra_fps)
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        camera.set(cv2.CAP_PROP_BRIGHTNESS, 60)
        camera.set(cv2.CAP_PROP_CONTRAST, 60)
        camera.set(cv2.CAP_PROP_SATURATION, 60)
        camera.set(cv2.CAP_PROP_EXPOSURE, 1)
        
        ret, img = camera.read( )
        self.img = img
        
        cv2.imshow("img", self.img)
        cv2.waitKey(1)
        camera.release( )
    
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
    
    def ball_recognition( self, mask, ratio, color ):
        ball = ballRecognition.Ball(mask, ratio)
        
        if color == "green":
            colors_param = (10, 40)
        elif color == "yellow":
            colors_param = (7, 20)
        else:
            colors_param = (10, 35)
        
        theta_up = 90
        theta_down = 90
        
        while True:
            self.get_img( )
            
            x, y, r = ball.findBall(self.img, *colors_param, color)
            if x == 0 and y == 0 and r == 0:
                continue
            
            x -= camra_width / 2
            y = camra_height / 2 - y
            if abs(y) < 3:
                y = 0
            if abs(x) < 3:
                x = 0
            
            up, down = self.calc_angle(x, y)
            
            theta_up += up
            theta_up = max(0, min(180, theta_up))
            
            theta_down += down
            theta_down = max(0, min(180, theta_down))
            
            self.servo_up.setAngle(theta_up)
            self.servo_down.setAngle(theta_down)
    
    def __del__( self ):
        GPIO.cleanup( )

if __name__ == '__main__':
    Solution = Solve(17, 4)
    
    while True:
        Solution.ball_recognition(5, 4, "green")