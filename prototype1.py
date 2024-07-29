from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyautogui
import mss
import mss.tools
import os
import time


class ebookToPDF:

    def __init__(self, root):

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.position = 0

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
        root.geometry("390x300")
        #root.resizable(width=False, height=False)

        #frame = ttk.Frame(root)        

        contents = ttk.Frame(root, borderwidth=5, padding="3 3 12 12", width=300, height=200)
        contents.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #font = ("Gulim", 8)

        ttk.Label(contents, text="이미지 좌측 상단 좌표", ).grid(column=1, row=1, sticky=W)
        ttk.Label(contents, textvariable=self.posDisplay1, width=10).grid(column=2, row=1, sticky=(W, E))
        ttk.Label(contents, text="이미지 우측 하단 좌표", ).grid(column=1, row=2, sticky=W)
        ttk.Label(contents, textvariable=self.posDisplay2, width=10).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(contents, text="좌표위치클릭", command=self.getPointerPosCallLeft).grid(column=3, row=1, sticky=(W, E))
        ttk.Button(contents, text="좌표위치클릭", command=self.getPointerPosCallRight).grid(column=3, row=2, sticky=(W, E))


        ttk.Label(contents, text="총 페이지 수").grid(column=1, row=3, sticky=W)
        ttk.Label(contents, text="PDF 이름").grid(column=1, row=4, sticky=W)
        ttk.Entry(contents, width=20, textvariable=self.pages).grid(column=3, row=3, sticky=E)
        ttk.Entry(contents, width=20, textvariable=self.name).grid(column=3, row=4, sticky=E)

        ttk.Label(contents, text="캡쳐속도").grid(column=1, row=5, sticky=W)
        ttk.Label(contents, textvariable=self.captureSpeed,width=3).grid(column=2, row=5, sticky=(W, E))
        ttk.Scale(contents, orient=HORIZONTAL, length=100, from_=0.1, to=1.0, variable=self.captureSpeed).grid(column=3, row=5, sticky=E)
        
        ttk.Progressbar(contents, orient=HORIZONTAL,length=30, mode='determinate', maximum = float(self.pages.get()), variable=self.progress).grid(column=1, row=6,columnspan=3,sticky=(W,E))

        ttk.Button(contents, text="작업 시작", command=self.captureCall).grid(column=1, row=7,columnspan=3, sticky=(W,E))
        ttk.Button(contents, text="저장 경로 설정", command=self.getDirPath).grid(column=1, row=8,columnspan=3, sticky=(W,E))
        ttk.Label(contents, text="경로", textvariable=self.dirPath).grid(column=1, row=9,columnspan=3, sticky=W)

        for child in contents.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    

    def getPointerPosCallLeft(self,*args): #Tkinter를 통해서 호출되는 메서드는 매개변수로 반드시 *args를 가지고 있어야 함.
        print("getPointerPosCallLeft")
        self.position = 1
        root.bind("<Key-space>", self.getPointerPos)

    def getPointerPosCallRight(self,*args):
        print("getPointerPosCallRight")
        self.position = 2
        root.bind("<Key-space>", self.getPointerPos)

    def getPointerPos(self,*args):
        posx,posy = pyautogui.position()
        if(self.position == 1):
            self.x1 = posx
            self.y1 = posy
            self.posDisplay1.set(str([posx,posy]))
        if(self.position == 2):
            self.x2 = posx
            self.y2 = posy
            self.posDisplay2.set(str([posx,posy]))
        root.bind("<Key-space>", None)

    def calculateRegion(self):
        #topLeftX, topRightY, width, height
        self.region = (self.x1,self.y1,self.x2-self.x1,self.y2-self.y1)

    def getDirPath(self, *args):
        self.dirPath.set(filedialog.askdirectory())
        print(self.dirPath.get())

    def captureCall(self, *args):
        self.calculateRegion()
        capture = Capture(self)
        capture.process()


class Capture:
    def __init__(self,ebookToPDF):
        self.ebookToPdf = ebookToPDF
        self.region = self.ebookToPdf.region
        self.pages = self.ebookToPdf.pages.get()
        self.name = self.ebookToPdf.name.get()
        self.dirpath = self.ebookToPdf.dirPath.get().replace("/","\\")
        self.captureSpeed = round(self.ebookToPdf.captureSpeed.get(),1)

        self.ebookToPdf.progress.set(0)


        self.count = 0

    def process(self):
        save_dir = os.path.dirname(self.dirpath)
        if not os.path.exists(save_dir):
            raise Exception("해당 경로가 발견되지 않음.")

        for i in range(self.pages):
            save_dir = self.dirpath+"\\"+self.name+str(self.count)+".png"
            self.count += 1

            self._capture(save_dir)
            self.ebookToPdf.progress.set(self.ebookToPdf.progress.get()+1)
            time.sleep(self.captureSpeed)

    def _capture(self, save_dir):
        
        with mss.mss() as sct:
            monitor = {"top": self.region[1], "left": self.region[0], "width": self.region[2], "height": self.region[3]}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_dir)

            print(self.count)
            



root = Tk()
ebookToPDF(root)#FeetToMeters인스턴스를 생성하는 과정에서 생성자 함수가 호출되고, root에 모든 설정을 끝냄.
root.mainloop()