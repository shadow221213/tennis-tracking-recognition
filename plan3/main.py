import math
import time

import cv2
import torch
from RPi import GPIO

import model.detector as detector
import servos
import util.utils as utl

camra_width = 640
camra_height = 640
camra_fps = 30

class Solve:
    
    def __init__( self, pin_up, pin_down ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.servo_up = servos.Servos_180(pin_up)
        self.servo_down = servos.Servos_180(pin_down)
        
        weights = './ball.pth'
        data = './ball.data'
        cfg = utl.load_datafile(data)
        
        device = torch.device("cuda" if torch.cuda.is_available( ) else "cpu")
        model = detector.Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
        model.load_state_dict(torch.load(weights, map_location = device))
        model.eval( )
        
        self.exit_flag = False
        
        self.theta_up = 90
        self.theta_down = 90
        
        self.cfg = cfg
        self.device = device
        self.model = model
    
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
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, camra_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camra_height)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FPS, camra_fps)
        
        ret, img = cap.read( )
        if ret:
            self.img = img.copy( )
        else:
            self.img = None
        cap.release( )
    
    def identify_one( self ):
        img = self.img
        if img is None:
            return
        
        cfg = self.cfg
        device = self.device
        
        src = cv2.resize(img, (cfg["width"], cfg["height"]), interpolation = cv2.INTER_LINEAR)
        src = src.reshape(1, cfg["height"], cfg["width"], 3)
        src = torch.from_numpy(src.transpose(0, 3, 1, 2)).to(device).float( ) / 255.0
        
        time1 = time.time( )
        preds = self.model(src)
        print(time.time( ) - time1)
        
        output = utl.handel_preds(preds, cfg, device)
        output_boxes = utl.non_max_suppression(output, conf_thres = 0.9, iou_thres = 0.9)
        
        # 加载label names
        LABEL_NAMES = []
        with open(cfg["names"], 'r') as f:
            for line in f.readlines( ):
                LABEL_NAMES.append(line.strip( ))
        
        h, w, _ = img.shape
        scale_h, scale_w = h / cfg["height"], w / cfg["width"]
        
        # 绘制预测框
        for box in output_boxes[0]:
            box = box.tolist( )
            
            obj_score = box[4]
            category = LABEL_NAMES[int(box[5])]
            
            x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
            x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(img, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)
            cv2.putText(img, category, (x1, y1 - 25), 0, 0.7, (0, 255, 0), 2)

if __name__ == '__main__':
    solve = Solve(17, 4)
    
    while True:
        solve.get_one_img( )
        solve.identify_one( )
        if solve.img is not None:
            cv2.imshow("img", solve.img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows( )