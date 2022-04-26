import csv
import time
import sys
from windows import *

def UI():
    #Variable for window size
    winWidth = 1080
    winHeight = 720
    win = newWindow("Journey Planner", winWidth, winHeight)
    ui = window()
    ui.setupUI(win)
    win.win.show()
    sys.exit(application.app.exec_())


if __name__ == '__main__':
    start = time.time()
    application = newApp()
    UI()
    end = time.time()
    print(end - start)