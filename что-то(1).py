#!/usr/bin/env python
#coding: utf-8

import time
from threading import Thread,Lock, Timer
from multiprocessing import Process,Manager
from samila import GenerativeImage
from tkinter import *
from PIL import ImageTk, Image

import glob
taskN=None
def genImg(i,ns):
    global taskN
    g=GenerativeImage()
    g.generate()
    g.plot()
    res =g.save_image(f"images/img_{i}.jpg")
    print(f"Картинка {i} сохранена")
    ns.taskN-=1
def onListClick (evt,canvas):
    w= evt.widget
    index = int(w.curselection()[0])
    img_path = w.get(index)
    print(img_path)

    img=Image.open(img_path)
    img=img.resize((300,300))
    img=ImageTk.PhotoImage(img)
    canvas["image"]=img
    canvas.image=img
    

    canvas.pack(side=LEFT)

threads=[]

def genImgs(N):
    global taskN, mgr,ns
    mgr=Manager()
    ns=mgr.Namespace()
    ns.taskN=N
    t1=time.time()
    
    print("Многопоточная обработка")

    for i in range(N):
        th=Process(target=genImg,args=(i,ns))
        threads.append(th)
    for i in range(N):
        threads[i].start()
    for i in range(N):
        threads[i].join()
    while ns.taskN>0:
       
        pass
    t2=time.time()
    print(f"Многопоточная обрабоотка заняла {t2-t1} сек.")

def  check_thread(thread,btn,imgList):
    if thread.is_alive():
        t=Timer(1,check_thread,args=(thread,btn,imgList))
        t.start()
    else:
        btn['state']='normal'
    imgs=glob.glob('images/*')
    imgList.delete(0,'end')
    for img in imgs:
        imgList.insert('end', img) 
def genButtonClick(btn,imgList):
    btn["state"]="disabled"
    imgGenThread= Thread(target=genImgs,args=(1,))
    imgGenThread.start()
    t=Timer(1,check_thread,args=(imgGenThread,btn,imgList))
    t.start()

def main():
    window = Tk()
    window.title('Генерация и просмотр изображений')
    window.geometry('500x500+300+300')
    imageListFrame= LabelFrame(window,text="Список изображений")

    imgList=Listbox(imageListFrame)
    imgList.pack()
    
    getButton=Button(imageListFrame,text='Генерация CARtinok', command=lambda: genButtonClick(getButton,imgList))
    getButton.pack()
    imageListFrame.pack(side=LEFT, fill='both', expand='yes')
    img=Image.new('RGB',(300,300), color=(255,255,255))
    img=img.resize((300,300))
    img=ImageTk.PhotoImage(img)
    canvas= Label(window, height=300,width=300,image=img)

    #canvas = Canvas(window, heigh=500,width=500,bg='white')
    canvas.pack(side = LEFT, fill='both', expand='yes')
    imgList.bind('<<ListboxSelect>>', lambda event,canvas=canvas:onListClick(event,canvas))
    def on_closing():
        for thread in threads:
            thread.kill()
            thread.terminate()
        window.destroy()

    window.mainloop()
if __name__ == "__main__":
    main()