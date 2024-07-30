#from pywinauto.keyboard import send_keys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyautogui
import mss
import mss.tools
import os
import time
import pydirectinput as pdi

#잘가....

class ebookToPDF:

    def __init__(self, root):

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.posDisplay1 = StringVar()
        self.posDisplay2 = StringVar()
        self.posDisplay1.set("[0,0]")
        self.posDisplay2.set("[0,0]")

        self.region = (0,0,0,0)#캡쳐 영역 설정

        self.pages = IntVar()

        self.name = StringVar()

        self.dirPath = StringVar()

        self.captureSpeed = DoubleVar()

        self.progress = DoubleVar()
        self.progress.set(0.0)

        root.title("ebookToPDF")
        root.geometry("390x310")
        #root.resizable(width=False, height=False)      

        contents = ttk.Frame(root, borderwidth=5, padding="3 3 12 12")
        contents.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(contents, text="이미지 좌측 상단 좌표", ).grid(column=1, row=1, sticky=W)
        ttk.Label(contents, text="이미지 우측 하단 좌표", ).grid(column=1, row=2, sticky=W)
        ttk.Label(contents, textvariable=self.posDisplay1, width=10).grid(column=2, row=1, sticky=(W, E))
        ttk.Label(contents, textvariable=self.posDisplay2, width=10).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(contents, text="좌표 설정", command=self.getPointerPosCallLeft).grid(column=3, row=1, sticky=(W, E))
        ttk.Button(contents, text="좌표 설정", command=self.getPointerPosCallRight).grid(column=3, row=2, sticky=(W, E))

        ttk.Label(contents, text="총 페이지 수").grid(column=1, row=3, sticky=W)
        ttk.Label(contents, text="파일 이름").grid(column=1, row=4, sticky=W)
        ttk.Entry(contents, width=20, textvariable=self.pages).grid(column=3, row=3, sticky=(W, E))
        ttk.Entry(contents, width=20, textvariable=self.name).grid(column=3, row=4, sticky=(W, E))

        ttk.Label(contents, text="캡쳐 간격(초)").grid(column=1, row=5, sticky=W)
        ttk.Label(contents, textvariable=self.captureSpeed,width=3).grid(column=2, row=5, sticky=(W, E))
        ttk.Scale(contents, orient=HORIZONTAL, length=100, from_=0.1, to=1.0, variable=self.captureSpeed).grid(column=3, row=5, sticky=(W,E))
        
        ttk.Progressbar(contents, orient=HORIZONTAL,length=30, mode='determinate', maximum = float(self.pages.get()), variable=self.progress).grid(column=1, row=6, columnspan=3, sticky=(W,E))

        ttk.Button(contents, text="작업 시작", command=self.captureCall).grid(column=1, row=7,columnspan=3, sticky=(W,E))
        ttk.Button(contents, text="저장 경로 설정", command=self.getDirPath).grid(column=1, row=8,columnspan=3, sticky=(W,E))
        ttk.Label(contents, text="경로", textvariable=self.dirPath, width=51).grid(column=1, row=9,columnspan=3, sticky=W)

        for child in contents.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    

    def getPointerPosCallLeft(self,*args): #Tkinter를 통해서 호출되는 메서드는 매개변수로 반드시 *args를 가지고 있어야 함.
        print("getPointerPosCallLeft")
        root.bind("<Key-space>", lambda event: self.getPointerPos(event,1))#바인드된 함수에 인자를 넘기려면 이런 방식으로 해야함.
        root.focus_set()  # root로 포커스 강제 이동, 스페이스바를 눌렀을 때 버튼이 계속 눌리던 문제를 해결

    def getPointerPosCallRight(self,*args):
        print("getPointerPosCallRight")
        root.bind("<Key-space>", lambda event: self.getPointerPos(event,2))
        root.focus_set()  # root로 포커스 강제 이동

    def getPointerPos(self,event,position):
        posx,posy = pyautogui.position()
        if(position == 1):
            self.x1 = posx
            self.y1 = posy
            self.posDisplay1.set(str([posx,posy]))
        if(position == 2):
            self.x2 = posx
            self.y2 = posy
            self.posDisplay2.set(str([posx,posy]))
        #root.unbind("<Key-space>") 스페이스바를 여러번 눌러서 좌표를 수정할 수 있게함.
        
    def calculateRegion(self):
        #topLeftX, topRightY, width, height
        self.region = (self.x1,self.y1,self.x2-self.x1,self.y2-self.y1)

    def getDirPath(self, *args):
        self.dirPath.set(filedialog.askdirectory())
        print(self.dirPath.get())

    def captureCall(self, *args, moveToNextPageMethod):
        time.sleep(2)#2초후 실행

        self.progress.set(0)#진행률 표시바 초기화
        self.calculateRegion()#캡처 영역 계산
        capture = Capture(self)#이 인스턴스를 통째로 넘겨줌.

        for i in range(self.pages.get()):
            capture.capture()
            self.progress.set(self.progress.get()+1)

            time.sleep(self.captureSpeed.get())
            moveToNextPageMethod()

    #다음페이지로 넘겨주는 함수들
    def moveToNextPageWithKey(self):
        pdi.keyDown("right")
        time.sleep(0.1)
        pdi.keyUp("right")

    def moveToNextPageWithClick(self):
        pdi.leftClick()



class Capture:
    def __init__(self,ebookToPDF):
        self.region = ebookToPDF.region
        self.pages = ebookToPDF.pages.get()
        self.name = ebookToPDF.name.get()
        self.dirpath = ebookToPDF.dirPath.get().replace("/","\\")
        self.captureSpeed = round(ebookToPDF.captureSpeed.get(),1)
        self.count = 0

    def capture(self):

        save_dir = self.dirpath+"\\"+self.name+str(self.count)+".png"
        self.count += 1

        with mss.mss() as sct:
            monitor = {"top": self.region[1], "left": self.region[0], "width": self.region[2], "height": self.region[3]}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_dir)
            



root = Tk()
ebookToPDF(root)#FeetToMeters인스턴스를 생성하는 과정에서 생성자 함수가 호출되고, root에 모든 설정을 끝냄.
root.mainloop()