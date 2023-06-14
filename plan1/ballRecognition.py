import cv2
import numpy as np

camra_width = 720
camra_height = 480

lower_black_yellow = np.array([26, 0, 0])
upper_black_yellow = np.array([34, 255, 46])
lower_black_red1 = np.array([0, 0, 0])
upper_black_red1 = np.array([10, 255, 46])
lower_black_red2 = np.array([156, 0, 0])
upper_black_red2 = np.array([180, 255, 46])

cnt = 3

class Ball:
    
    def __init__( self, mask = 5, ratio = 4 ):
        self.mask = mask
        self.ratio = ratio
        self.colors = { "white":                                                                {
                "lower": np.array([0, 0, 46]), "upper": np.array([180, 43, 255]) }, "green":    {
                "lower": np.array([40, 40, 40]), "upper": np.array([77, 255, 255]) }, "orange": {
                "lower": np.array([11, 43, 46]), "upper": np.array([25, 255, 255]) }, "yellow": {
                "lower": np.array([26, 43, 46]), "upper": np.array([34, 255, 255]) }, "red":    {
                "lower":      np.array([0, 43, 46]), "upper": np.array([10, 255, 255]),
                "else_lower": np.array([156, 43, 46]), "else_upper": np.array([180, 255, 255]) } }
    
    def findBall( self, img, radius_min = 0, radius_max = 0, color = "white" ):
        """
        从图像(BRG)中找到球。
        :param img: 用于查找球的图像。
        :return: 小球所在的x, y坐标和半径。
        """
        
        lowThreshold = 100
        
        cv2.imshow("img", img)
        cv2.waitKey(1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gas = cv2.GaussianBlur(hsv, (self.mask, self.mask), 0, 0)
        if color in self.colors:
            color_data = self.colors[color]
            binary = cv2.inRange(gas, color_data["lower"], color_data["upper"])
            
            if "else_lower" in color_data:
                binary1 = cv2.inRange(gas, color_data["else_lower"], color_data["else_upper"])
                binary = cv2.add(binary, binary1)
        else:
            raise ValueError("Invalid color specified.")
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.mask, self.mask))
        Open = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        cay = cv2.Canny(Open, lowThreshold, lowThreshold * self.ratio, apertureSize = self.mask,
                        L2gradient = True)
        circles = cv2.HoughCircles(cay, cv2.HOUGH_GRADIENT, 1, 50, param1 = 100, param2 = 25,
                                   minRadius = radius_min * self.ratio,
                                   maxRadius = radius_max * self.ratio)
        
        x, y, r = 0, 0, 0
        
        if circles is not None:
            cir = []
            
            for circle in circles[0]:
                xx, yy, rr = map(int, circle)
                is_valid = Open[yy][xx] == 255
                if not is_valid:
                    cnt = sum([Open[min(yy + rr // 2, camra_height - 1)][xx] != 255,
                               Open[max(yy - rr // 2, 0)][xx] != 255,
                               Open[yy][min(xx + rr // 2, camra_width - 1)] != 255,
                               Open[yy][max(xx - rr // 2, 0)] != 255])
                    is_valid = cnt >= 3
                if is_valid:
                    cir.append((xx, yy, rr))
            
            if cir:
                x, y, r = map(int, np.mean(cir, axis = 0))
                cv2.circle(img, (x, y), r, (0, 255, 0), 5)
                cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
                cv2.imshow("img", img)

        global cnt
        
        if cv2.waitKey(1000) == 32:
            cv2.imwrite("./train/" + str(cnt) + ".jpg", self.img)
            cnt += 1
        
        return x, y, r
