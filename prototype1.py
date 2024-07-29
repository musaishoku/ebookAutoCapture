from tkinter import *
from tkinter import ttk
import pyautogui
import time


class ebookToPDF:

    def __init__(self, root):

        root.title("ebookToPDF")

        mainframe = ttk.Frame(root, padding="3 3 12 12",width=300, height=200)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.positin = 0

        self.posDisplay1 = StringVar()
        self.posDisplay2 = StringVar()
        self.posDisplay1.set("[0,0]")
        self.posDisplay2.set("[0,0]")

        self.region = (0,0,0,0)#캡쳐 영역 설정

        progress = DoubleVar()
        progress.set(0.0)

        ttk.Label(mainframe, text="이미지 좌측 상단 좌표").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="이미지 우측 하단 좌표").grid(column=1, row=2, sticky=W)

        ttk.Label(mainframe, textvariable=self.posDisplay1).grid(column=2, row=1, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.posDisplay2).grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="좌표위치클릭", command=self.getPointerPosCallLeft).grid(column=3, row=1, sticky=E)
        ttk.Button(mainframe, text="좌표위치클릭", command=self.getPointerPosCallRight).grid(column=3, row=2, sticky=E)


        ttk.Label(mainframe, text="총 페이지 수").grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text="PDF 이름").grid(column=1, row=4, sticky=W)

        ttk.Entry(mainframe, width=20, textvariable=None).grid(column=3, row=3, sticky=E)
        ttk.Entry(mainframe, width=20, textvariable=None).grid(column=3, row=4, sticky=E)


        ttk.Label(mainframe, text="캡쳐속도").grid(column=1, row=5, sticky=W)
        ttk.Label(mainframe, textvariable=None).grid(column=2, row=5, sticky=(W, E))
        ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=0.1, to=1.0).grid(column=3, row=5, sticky=E)

        
        ttk.Progressbar(mainframe, orient=HORIZONTAL, length=500, mode='determinate', maximum = 100.0, variable=progress).grid(column=2, row=6, sticky=(W,E))

        
        ttk.Button(mainframe, text="작업 시작", command=None).grid(column=2, row=7, sticky=(W,E))
        

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        # feet_entry.focus()

        root.bind("<Key-space>", lambda : print("Hello World"))
    

    def getPointerPosCallLeft(self,*args): #Tkinter를 통해서 호출되는 메서드는 매개변수로 반드시 *args를 가지고 있어야 함.
        print("getPointerPosCallLeft")
        self.position = 1
        root.bind("<Key-space>", self.getPointerPos)

    def getPointerPosCallRight(self,*args):
        print("getPointerPosCallRight")
        self.position = 2
        root.bind("<Key-space>", self.getPointerPos)

    def getPointerPos(self):
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

    def calculateRegion(self,*args):
        self.region = (self.x1,self.y1,self.x2,self.y2)



root = Tk()
ebookToPDF(root)#FeetToMeters인스턴스를 생성하는 과정에서 생성자 함수가 호출되고, root에 모든 설정을 끝냄.
root.mainloop()