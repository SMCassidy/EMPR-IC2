# Use Tkinter for python 2, tkinter for python 3
import Tkinter as tk
from threading import Thread, Lock
from time import sleep
from random import randint
import serial

LIGHTS = 6
TIME = 0.2

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = Canvas(self, width=625, height=325, bd=2, bg='#222222')
        self.canvas.config(highlightbackground="#111111")
        self.console = Console(self, height=5, width=75, relief="raised", \
                                                bg='#444444', fg='#BBBBBB')
        self.console.config(highlightbackground="#111111")
        self.pack(fill="both", side="right", expand=True)
        self.channels = { 0:255,  1:255,  2:255,  3:255,  4:255,  5:255, \
                          6:255,  7:255,  8:255,  9:255, 10:255, 11:255, \
                         12:255, 13:255, 14:255, 15:255, 16:255, 17:255  }
        for i in range(512):
            self.channels[i] = 255

        self.lights = self.light_builder()
        self.initial_colors = ['#DD6666', '#DD8833', '#DDDD33', \
                               '#66DD66', '#6666DD', '#DD66DD' ]
        for i in range(LIGHTS):
            self.lights[i].setColor(self.initial_colors[i])
        global randlock, serlock
        randlock.acquire()
        serlock.acquire()
#        self.ser = serial.Serial('/dev/ttyACM0')
 #       self.ser.baudrate = 250000
  #      self.ser.stopbits = 1
   #     self.ser.timeout = 1

    def light_builder(self):
        x1 = 50
        x2 = 150
        y = 150
        lights = []
        initial_channels = [[0, 1, 2],[ 3, 4, 5],[ 6, 7, 8], \
                            [9,10,11],[12,13,14],[5,10,14]]
        for i in range(LIGHTS):
            if i == 3:
                y = 305
                x1 = 50
                x2 = 150
            lights.append(Light(self, x1, x2, y, initial_channels[i]))
            x1 += 205
            x2 += 205
        return lights

    def generator(self):

        '''
        Produces random values and adds them to the global channels dict.
        Ideally the dict will be updated by the incoming serial read thread.
        '''

        sleep(TIME)
        r = lambda: randint(0,255)
        while True:
            try:
                with randlock:
                    for c in self.channels:
                        self.channels[c] = r()
                    sleep(0.2)
            except:
                return

    def updater(self):

        '''
        Accesses channels dictionary for current value for each channel.
        Updates the three lights according to the color value hexstring.
        '''

        try:
            while True:
                colors = ['','','','','','']
                current_channels = []
                c = lambda r, g, b: '#%02X%02X%02X' % (r,g,b)
                #Get Light addresses, Produce hexstring, Update light
                for i in range(len(self.lights)):
                    current_channels.append(self.lights[i].getChannels())
                    r = self.channels[current_channels[i][0]]
                    g = self.channels[current_channels[i][1]]
                    b = self.channels[current_channels[i][2]]
                    colors[i] = c(r,g,b)
                    with lock:
                        self.lights[i].setColor(colors[i])
                self.parent.control.UpdateColourLabels()
                sleep(TIME)
        except:
            return

    def serial(self):

        '''
        Reads from serial and updates global channels dict.
        '''

        while True:
            line = self.ser.readline()
            line = line.split('-')
            line = line[1:-1]
            for i in range(len(line)):
                try:
                    self.channels[i] = int(line[i])
                except:
                    continue

class Light(object):
    def __init__(self, parent, x1, x2, y, channels):
        self.parent = parent
        self.color = ''
        self.channels = channels
        yl = y - 125
        self.stand = self.parent.canvas.create_polygon([x1,y, x1+((x2-x1)/2), \
                                          y-75, x2, y], width=2,fill='#000000')
        self.light = self.parent.canvas.create_oval(x1, yl, x2, yl+100, \
                                        fill="white", outline='black', width=7)
    def setColor(self,color):
        self.color = color
        self.parent.canvas.itemconfig(self.light,fill=color)

    def getColor(self):
        return self.color

    def getChannels(self):
        return self.channels

    def setChannels(self, channels):
        self.channels = channels

class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", expand=True, side="left")
        self.presslock = False
        self.gen = True
        self.serial = False
        title = tk.Label(self, text="  EMPR IC2  \n\n DMX-512 ", bd=3, \
                                    font="bold", bg="black", fg="white")
        title.pack(fill="both")
        title.config(highlightbackground="red")
        self.colours = tk.Frame(self)
        self.colours.pack(fill="x", side="bottom")
        self.w_blue = tk.Label(self.colours, text="Blue", bg="blue", fg="white", font = "Courier 10 bold")
        self.w_blue.pack(fill="x", side="bottom")
        self.w_green = tk.Label(self.colours, text="Green", bg="green", fg="black", font = "Courier 10 bold")
        self.w_green.pack(fill="x", side="bottom")
        self.w_red = tk.Label(self.colours, text="Red", bg="red", fg="white", font = "Courier 10 bold")
        self.w_red.pack(fill="x", side="bottom")

        test = tk.Button(self,text="Start", command=self.Start)
        test.pack(fill="x")
        gen = tk.Button(self, text="Random", command=self.gen_begin)
        gen.pack(fill="x")
        gen = tk.Button(self, text="Serial", command=self.serial_begin)
        gen.pack(fill="x")
        pause = tk.Button(self, text="Pause", command=self.Pressed)
        pause.pack(fill="x")

        #Enter big empty frame here
        frm = tk.Frame(self, height=38, bg='#333333')
        frm.pack(fill="x")

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="x")

        self.var = tk.StringVar(self)
        self.drop = tk.OptionMenu(self.list_frame,self.var, \
                    'Light 1','Light 2', 'Light 3', 'Light 4', 'Light 5', 'Light 6')
        self.drop.grid()

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill="x")

        set_btn = tk.Button(self.entry_frame, text="Set", command=self.Update)
        set_btn.pack(side="right")
        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(fill="both")

        frm = tk.Frame(self, height=20, bg='#333333')
        frm.pack(fill="x")

        self.info = tk.Text(self, height=3, width=20,relief="raised", bg='#444444', fg='#BBBBBB')
        self.info.pack(fill="x")

        #We need a text output to show current light, current channels, current colour

    def gen_begin(self):
        global randlock

        if self.gen == False:
            randlock.acquire()
            self.gen = True
            self.parent.main.console.insert_text('Random paused...')
        else:
            randlock.release()
            self.gen = False
            self.parent.main.console.insert_text('Random colours...')

    def serial_begin(self):
        global lock
        if not self.serial:
            lock.release()
            self.serial = True
            self.parent.main.console.insert_text('Serial begin...')

    def Start(self):
        gen_thread = thread_launch(main_app.main.generator)
        update_thread = thread_launch(main_app.main.updater)

        # should add updated bytes to queue from serial
        #serial_thread = thread_launch(main_app.main.serial)

    def Update(self):

        self.Set()

        light = self.var.get()
        lightnum = int(light[-1]) - 1

        self.UpdateInfo('Light ' + str(int(lightnum) +1) + ':\n'\
                        'Color:' + str(self.parent.main.lights[lightnum].getColor()) + '\n'\
                        'Channels:' + str(self.parent.main.lights[lightnum].getChannels()))

    def UpdateInfo(self, text):
        self.info.delete(1.0,4.0)
        self.info.insert(1.0, text)

    def UpdateColourLabels(self):
        light = self.var.get()
        try:
            lightnum = int(light[-1]) - 1
        except:
            return
        text = ['Red:    ', 'Green:    ', 'Blue:    ']
        labels = [self.w_red, self.w_green, self.w_blue]
        chans = self.parent.main.lights[lightnum].getChannels()
        for i in range(3):
            val = '0x%02x' % self.parent.main.channels[chans[i]]
            labels[i]['text'] = text[i] + val
        return

    def Set(self):
        text = self.entry.get()
        text = text.split(',')
        new_channels = []
        valid = True

        if len(text) is not 3:
            valid = False

        for i in text:
            try:
                i = int(i)
                if i < 0 or i > 512:
                    self.parent.main.console.insert_text("Invalid input - channels between 0-512")
                    valid = False
                new_channels.append(i)
            except:
                self.parent.main.console.insert_text("Invalid input - only numeric input")
                return
        if valid:
            light = self.var.get()
            lightnum = int(light[-1]) - 1
            self.parent.main.lights[lightnum].setChannels(new_channels)
            self.parent.main.console.insert_text("Light " + str(lightnum + 1) + \
                                    " channels updated to " + str(new_channels))

    def Pressed(self):
        global lock

        if not self.presslock:
            lock.acquire()
            self.presslock = True
            self.parent.main.console.insert_text('Paused...')
        else:
            lock.release()
            self.presslock = False
            self.parent.main.console.insert_text('Unpaused...')

class Console(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", side="bottom")
    def insert_text(self, text):
        self.insert(1.0, ' ' + text + '\n')
        self.delete(6.0,7.0)

class Canvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.pack(fill="both", side="top", expand=True)

class Menu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.menu = tk.Menu(self)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main = Main(self, width=625, height=350)
        self.main.config(highlightbackground="#111111")
        self.control = ControlPanel(self, bg="#333333")

def thread_launch(func):
    thread = Thread(target=func)
    thread.setDaemon(True)
    thread.start()
    return thread

def main_func():
    root.mainloop()

if __name__ == "__main__":
    randlock = Lock()
    serlock = Lock()
    lock = Lock()
    root = tk.Tk()
    root.wm_title("DMX-512 Project")
    main_app = MainApplication(root, width=600, height=350)
    main_app.pack(side="top", fill="both", expand=True)

    root.mainloop()
#    main_thread = thread_launch(main_func)
   # gen_thread = thread_launch(main_app.main.generator)
    #update_thread = thread_launch(main_app.main.updater)

    #main_thread.join()
