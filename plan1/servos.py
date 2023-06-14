import time

import RPi.GPIO as GPIO

class Servos_180:
    """
    180度舵机
    """
    
    def __init__( self, pin ):
        """
        :param pin: 设置舵机的引脚
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.angle2DutyCycle(90))
        time.sleep(0.05)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.005)
    
    def angle2DutyCycle( self, angle ):
        """
        角度转换为脉冲占空比
        :param angle: 角度
        :return: 脉冲宽度
        """
        dutyCycle = int(angle / 18.0 + 2.5)
        return dutyCycle
    
    def setAngle( self, angle ):
        """
        :param angle: 设置舵机的角度
        """
        dutyCycle = self.angle2DutyCycle(angle)
        self.pwm.ChangeDutyCycle(dutyCycle)
        time.sleep(0.05)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.005)
    
    def destroy( self ):
        self.pwm.stop( )
