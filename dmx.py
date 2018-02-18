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
        self.channels = {0:255, 1:128, 2:64, \
                         3:128, 4:64, 5:255, \
                         6:64, 7:255, 8:128, }

        self.lights = self.light_builder()

    def light_builder(self):
        x1 = 50
        x2 = 150
        lights = []
        initial_channels = [[0,1,2],[3,4,5],[6,7,8]]
        for i in range(3):
            lights.append(Light(self, x1,x2, initial_channels[i]))
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
            for c in self.channels:
                self.channels[c] = r()
            sleep(0.2)


    def updater(self):

        '''
        Accesses channels dictionary for current value for each channel.
        Updates the three lights according to the color value hexstring.
        '''

        try:
            current_channels = [self.lights[0].getChannels(), \
                             self.lights[1].getChannels(), \
                             self.lights[2].getChannels()]

            while True:

                colors = ['','','']

                c = lambda r, g, b: '#%02X%02X%02X' % (r,g,b)

                #Produce hexstring
                for i in range(3):
                    r = self.channels[current_channels[i][0]]
                    g = self.channels[current_channels[i][1]]
                    b = self.channels[current_channels[i][2]]
                    colors[i] = c(r,g,b)

                #Update lights
                if main_thread.is_alive():
                    with lock:
                        self.lights[0].change(colors[0])
                        self.lights[1].change(colors[1])
                        self.lights[2].change(colors[2])

                sleep(0.2)

        except:
            return


class Light(object):
    def __init__(self, parent, x1, x2, channels):
        self.parent = parent
        self.color = ''
        self.channels = channels
        self.stand = self.parent.canvas.create_polygon([x1,225, x1+((x2-x1)/2), 150, x2, 225], width=2,fill='#000000')
        self.light = self.parent.canvas.create_oval(x1, 100, x2, 200, fill="white", outline='black', width=7)

    def change(self,color):
        self.parent.canvas.itemconfig(self.light,fill=color)

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
        title = tk.Label(self, text="  EMPR IC2  \n\n DMX-512 ", bd=3, font="bold", bg="black", fg="white")
        title.pack(fill="both")
        title.config(highlightbackground="red")
        w = tk.Label(self, text="Red", bg="red", fg="white")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Green", bg="green", fg="black")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Blue", bg="blue", fg="white")
        w.pack(fill="x", side="bottom")
        pause = tk.Button(self, text="Pause", command=self.Pressed)
        pause.pack(fill="x")

    def Pressed(self):
        global lock
        if not self.presslock:
            lock.acquire()
            self.presslock = True
        else:
            lock.release()
            self.presslock = False

        self.parent.main.console.insert_text('Paused.')

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
