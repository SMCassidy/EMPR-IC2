from Tkinter import *
from time import *
from threading import Thread
import random
import Queue

colors = {0:'#FF0000', 1:'#FF7F00', 2:'#FFFF00', 3:'#00FF00', 4:'#0000FF', 5:'#4B0082', 6:'#9400D3'}


class light(object):
    def __init__(self, color, x1, x2):
        self.notch = 0
        self.color = color
        self.channels = []
        self.stand = c.create_polygon([x1,225, x1+((x2-x1)/2), 150, x2, 225], width=2,fill='#000000')
        self.light = c.create_oval(x1, 100, x2, 200, fill=color)

    def change(self,color):
        c.itemconfig(self.light,fill=color)

    def getChannels(self):
        return self.channels

    def getNotch(self):
        return self.notch

    def setNotch(self, notch):
        self.notch = notch

class backlight(object):
    def __init__(self, x1, x2):
        self.light = c.create_oval(x1, 97, x2, 203, fill='#000000')

def pressed():                          #function
    #print 'buttons are cool'
    notch = light1.getNotch()
    t.insert(INSERT, 'notch:' + str(notch) + ' button pressed...\n')
    light1.change(colors[notch])
    light1.setNotch((notch+1)%6)
    light2.change(colors[(notch-1)%6])
    light3.change(colors[(notch-2)%6])

def changer():
    sleep(1)
    r = lambda: random.randint(0,255)
    c = lambda: '#%02X%02X%02X' % (r(),r(),r())
    while True:
        #color = '#%02X%02X%02X' % (r(),r(),r())
        light1.change(c())
        light2.change(c())
        light3.change(c())
        sleep(0.5)

root = Tk()                             #main window
frame = Frame(root)
c = Canvas(frame, width=600, height=325, bd=4, bg='#222222')
frame.pack()
c.pack()

#Generate lights
back1 = backlight(90, 210)
back2 = backlight(240, 360)
back3 = backlight(390, 510)
light1 = light('#AA0000', 100,200)
light2 = light('#00AA00', 250, 350)
light3 = light('#0000AA', 400, 500)

t = Text(frame, height=5, width=75, bg='#444444', fg='#BBBBBB')
t.pack()

button = Button(frame, text = 'Press', command = pressed)
button.pack(pady=10, padx = 20)
#pressed()

mainThread = Thread(target=changer)
mainThread.setDaemon(True)
mainThread.start()

root.mainloop()
