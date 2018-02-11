from Tkinter import *
from time import *

class light(object):
    def __init__(self, color, x1, x2):
        self.color = color
        self.channels = []
        self.stand = c.create_polygon([x1,225, x1+((x2-x1)/2), 150, x2, 225], width=2,fill='#000000')
        self.light = c.create_oval(x1, 100, x2, 200, fill=color)

    def changeColor(self,color):
        c.itemconfig(self.light,fill=color)

    def getChannels(self):
        return self.channels

class backlight(object):
    def __init__(self, x1, x2):
        self.light = c.create_oval(x1, 97, x2, 203, fill='#000000')

def pressed():                          #function
        print 'buttons are cool'
        light1.changeColor('#FFFFFF')

root = Tk()                             #main window
frame = Frame(root)
c = Canvas(frame, width=600, height=325, bd=4, bg='#222222')
frame.pack()
c.pack()

#Generate stands
#stand = c.create_polygon([85,225,150,150,215,225], width=2,fill='#000000')

#Generate lights
back1 = backlight(90, 210)
back2 = backlight(240, 360)
back3 = backlight(390, 510)
light1 = light('#AA0000', 100,200)
light2 = light('#00AA00', 250, 350)
light3 = light('#0000AA', 400, 500)
#x1=90
#x2=210
#100, 100, 500, 500, 300, 300, 200, 200,

t = Text(frame, height=5, width=75, bg='#444444', fg='#BBBBBB')
t.pack()

button = Button(frame, text = 'Press', command = pressed)
button.pack(pady=10, padx = 20)
#pressed()
root.mainloop()
