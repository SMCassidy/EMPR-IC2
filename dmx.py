# Use Tkinter for python 2, tkinter for python 3
import Tkinter as tk
from threading import Thread, Lock
from time import sleep
from random import randint

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = Canvas(self, width=625, height=325, bd=2, bg='#222222')
        self.canvas.config(highlightbackground="#111111")
        self.console = Console(self, height=6, width=75, relief="raised", bg='#444444', fg='#BBBBBB')
        self.console.config(highlightbackground="#111111")
        self.pack(fill="both", side="right", expand=True)
        self.channels = { 0:255,  1:255,  2:255,  3:255,  4:255,  5:255, \
                          6:255,  7:255,  8:255,  9:255, 10:255, 11:255, \
                         12:255, 13:255, 14:255, 15:255, 16:255, 17:255  }

        self.lights = self.light_builder()
        self.initial_colors = ['#DD6666', '#DD8833', '#DDDD33', \
                               '#66DD66', '#6666DD', '#DD66DD' ]
        for i in range(6):
            self.lights[i].change(self.initial_colors[i])

    def light_builder(self):
        x1 = 50
        x2 = 150
        y = 150
        lights = []
        initial_channels = [[0, 1, 2],[ 3, 4, 5],[ 6, 7, 8], \
                            [9,10,11],[12,13,14],[15,16,17]]
        for i in range(6):
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

        sleep(0.2)
        r = lambda: randint(0,255)
        while True:
            try:
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
                        self.lights[i].change(colors[i])

                sleep(0.2)

        except:
            return


class Light(object):
    def __init__(self, parent, x1, x2, y, channels):
        self.parent = parent
        self.color = ''
        self.channels = channels
        yl = y - 125
        self.stand = self.parent.canvas.create_polygon([x1,y, x1+((x2-x1)/2), y-75, x2, y], width=2,fill='#000000')
        self.light = self.parent.canvas.create_oval(x1, yl, x2, yl+100, fill="white", outline='black', width=7)

    def change(self,color):
        self.parent.canvas.itemconfig(self.light,fill=color)

    def getChannels(self):
        return self.channels

    def setChannels(self, channels):
        self.channels = channels


class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        global lock
        lock.acquire()
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", expand=True, side="left")
        self.presslock = True
        self.gen = False
        title = tk.Label(self, text="  EMPR IC2  \n\n DMX-512 ", bd=3, font="bold", bg="black", fg="white")
        title.pack(fill="both")
        title.config(highlightbackground="red")
        w = tk.Label(self, text="Red", bg="red", fg="white")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Green", bg="green", fg="black")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Blue", bg="blue", fg="white")
        w.pack(fill="x", side="bottom")
        gen = tk.Button(self, text="Random", command=self.gen_begin)
        gen.pack(fill="x")
        pause = tk.Button(self, text="Pause", command=self.Pressed)
        pause.pack(fill="x")
        test = tk.Button(self,text="Test", command=self.Test)
        test.pack(fill="x")

    def gen_begin(self):
        global lock
        if not self.gen:
            lock.release()
            self.gen = True
            self.presslock = False
            self.parent.main.console.insert_text('Random colours...')

    def Test(self):
        self.parent.main.console.insert_text(str(len(self.parent.main.lights)))

    def Pressed(self):
        global lock
        if self.gen == False:
            return
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
        self.insert(6.0, text + '\n')

class Canvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.pack(fill="both", side="top", expand=True)

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
    lock = Lock()
    root = tk.Tk()
    root.wm_title("DMX-512 Project")
    main_app = MainApplication(root, width=600, height=350)
    main_app.pack(side="top", fill="both", expand=True)

    main_thread = thread_launch(main_func)
    gen_thread = thread_launch(main_app.main.generator)
    update_thread = thread_launch(main_app.main.updater)
    #main_app.main.lights[0].change("red")
    main_thread.join()
