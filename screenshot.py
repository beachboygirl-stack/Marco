import os
import sys
import time
from PIL import Image
from PIL import ImageGrab
import ctypes

SaveDirectory =r'C:\screenshot'

# 如果資料匣不存在，自動建立
os.makedirs(SaveDirectory, exist_ok=True)

# 隱藏命令提示字元視窗
whnd = ctypes.windll.kernel32.GetConsoleWindow() 
if whnd != 0: 
    ctypes.windll.user32.ShowWindow(whnd, 0) 
    ctypes.windll.kernel32.CloseHandle(whnd)
# 擷取螢幕並儲存
for i in range(1):
    img = ImageGrab.grab()
    saveas = os.path.join(SaveDirectory,time.strftime("%Y-%m-%d_%H-%M-%S")+'.jpg')
    img.save(saveas)
    time.sleep(3)
