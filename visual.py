from Tkinter import *
from time import *
from threading import Thread, Lock
import random
import Queue

colors = {0:'#FF0000', 1:'#FF7F00', 2:'#FFFF00', 3:'#00FF00', 4:'#0000FF', 5:'#4B0082', 6:'#9400D3'}
channels = {0:255, 1:128, 2:64, \
            3:128, 4:64, 5:255, \
            6:64, 7:255, 8:128, }
presslock = False

class light(object):
    def __init__(self, color, x1, x2, channels):
        self.notch = 0
        self.color = color
        self.channels = channels
        self.stand = c.create_polygon([x1,225, x1+((x2-x1)/2), 150, x2, 225], width=2,fill='#000000')
        self.light = c.create_oval(x1, 100, x2, 200, fill=color, outline='black', width=7)

    def change(self,color):
        c.itemconfig(self.light,fill=color)

    def getChannels(self):
        return self.channels

    def getNotch(self):
        return self.notch

    def setNotch(self, notch):
        self.notch = notch

def pressed():                          #function
    #print 'buttons are cool'
    global presslock
    if not presslock:
        lock.acquire()
        presslock = True
    else:
        lock.release()
        presslock = False

    notch = light1.getNotch()
    t.insert(INSERT, 'notch:' + str(notch) + ' button pressed...\n')
    light1.change(colors[notch])
    light1.setNotch((notch+1)%6)
    light2.change(colors[(notch-1)%6])
    light3.change(colors[(notch-2)%6])

def generator():

    '''
    Produces random values and adds them to the global channels dict.
    Ideally the dict will be updated by the incoming serial read thread.
    '''

    sleep(0.2)
    global channels
    r = lambda: random.randint(0,255)
    while True:
        for c in channels:
            channels[c] = r()
        sleep(0.2)

def updater():

    '''
    Accesses channels dictionary for current value for each channel.
    Updates the three lights according to the color value hexstring.
    '''

    sleep(0.2)

    global channels
    try:
        temp_channels = [light1.getChannels(), \
                         light2.getChannels(), \
                         light3.getChannels()]

        while True:

            colors = ['','','']

            c = lambda r, g, b: '#%02X%02X%02X' % (r,g,b)

            #Produce hexstring
            for i in range(3):
                r = channels[temp_channels[i][0]]
                g = channels[temp_channels[i][1]]
                b = channels[temp_channels[i][2]]
                colors[i] = c(r,g,b)

            #Update lights
            if main_thread.is_alive():
                with lock:
                    light1.change(colors[0])
                    light2.change(colors[1])
                    light3.change(colors[2])

            sleep(0.2)

    except:
        return

lock = Lock()

root = Tk()                             #main window
root.wm_title("DMX-512 Project")
frame = Frame(root)
c = Canvas(frame, width=600, height=325, bd=4, bg='#222222')
frame.pack()
c.pack()

#Generate lights
light1 = light('#AA0000', 100, 200, [0,1,2])
light2 = light('#00AA00', 250, 350, [3,4,5])
light3 = light('#0000AA', 400, 500, [6,7,8])

t = Text(frame, height=5, width=75, bg='#444444', fg='#BBBBBB')
t.pack()

button = Button(frame, text = 'Pause', command = pressed)
button.pack(pady=10, padx = 20)

gen_thread = Thread(target=generator)
gen_thread.setDaemon(True)
gen_thread.start()

update_thread = Thread(target=updater)
update_thread.setDaemon(True)
update_thread.start()

def main():
    root.mainloop()

main_thread = Thread(target=main)
main_thread.setDaemon(True)
main_thread.start()
main_thread.join()
