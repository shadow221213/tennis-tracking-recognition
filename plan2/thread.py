import threading
from typing import Callable, Any

class MyThread(threading.Thread):
    """
    用于多线程
    """
    
    def __init__(self, func: Callable, args: tuple):
        """
        :param func: 函数名
        :param args: 参数
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result: Any = None
    
    def run( self ):
        self.result = self.func(*self.args)
    
    def getResult( self ) -> Any:
        return self.result