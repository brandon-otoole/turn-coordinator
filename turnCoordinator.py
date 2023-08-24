#! /usr/bin/env python3

from configparser import ConfigParser

#Read config.ini file
configData = ConfigParser()
configData.read("config.ini")
socketConfig = configData["READ_SOCKET"]
UDP_ADDRESS = socketConfig["address"]
UDP_PORT = int(socketConfig["port"])

import tkinter
import threading
import time

from base64 import b16encode
from queue import Queue

from SocketListener import SocketListener
from CoordinatorGraphic import Coordinator
from My2D import rotatePoly, movePoly, degToRad

def grayscale(v):
    return(b'#' + b16encode(bytes((v,v,v))))
def rgb(r, g, b):
    return(b'#' + b16encode(bytes((r,g,b))))

# a dummy thread to make state changes in the background
class stateLoop(threading.Thread):
    def __init__(self, tc, dt, dataPipe):
        threading.Thread.__init__(self)
        self.tc = tc
        self.dt = dt
        self.dataPipe = dataPipe

    def run(self):
        try:
            #nextUpdate = time.time() + self.dt
            while True:
                while self.dataPipe.empty():
                #while time.time() < nextUpdate:
                    #time.sleep(dtGraphics/100)
                    pass

                #nextUpdate = time.time() + self.dt

                p, q, r, na, na, na, na, na = self.dataPipe.get()

                self.tc.theta = degToRad(r*5)

        except KeyboardInterrupt:
            sys.exit()

def main(height, width, dtState, dtGraphics):
    darkGray = grayscale(75)

    window = tkinter.Tk()
    window.title("Tkinter Animation Demo")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{width}x{height}')

    canvas = tkinter.Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill="both", expand=True)

    # x,  y,  theta
    tc = Coordinator(400, 400, 0)

    # create and begin the state update loop
    dataPipe = Queue()

    bgLoop = stateLoop(tc, dtState, dataPipe)
    bgLoop.start()

    socketListener = SocketListener(UDP_ADDRESS, UDP_PORT)
    socketListener.subscribe(16, lambda x: dataPipe.put(x))
    socketListener.start()

    # draw the outer ring
    canvas.create_oval(0, 0, 800, 800, fill=darkGray)

    # draw the shadow of the outer ring
    sw = 35
    step = 2
    for i in range(0, sw):
        color = grayscale(i*step)
        canvas.create_oval(75+i, 75+i, 725-i, 725-i, fill=color, width=0)

    # draw the background of the instrument face
    canvas.create_oval(75+sw, 75+sw, 725-sw, 725-sw, fill=darkGray, width=0)

    # base geometry for a turn tic polygon
    tic = [-25, -10, 25, -10, 25, 10, -25, 10]

    # create the left normal tic
    lTic = [ v for v in tic ]
    movePoly(lTic, 350, 0)
    movePoly(lTic, 400, 400)
    canvas.create_polygon(*lTic, fill="white")

    # create the right normal tic
    rTic = [ v for v in tic ]
    movePoly(rTic, -350, 0)
    movePoly(rTic, 400, 400)
    canvas.create_polygon(*rTic, fill="white")

    # create the left turn tic
    llTic = [ v for v in tic ]
    movePoly(llTic, 350, 0)
    rotatePoly(llTic, degToRad(15))
    movePoly(llTic, 400, 400)
    canvas.create_polygon(*llTic, fill="white")

    # create the right turn tic
    rrTic = [ v for v in tic ]
    movePoly(rrTic, -350, 0)
    rotatePoly(rrTic, degToRad(-15))
    movePoly(rrTic, 400, 400)
    canvas.create_polygon(*rrTic, fill="white")

    # draw the coordinator shadow
    shadowColor = grayscale(35)
    shadowOffset = 12
    sw1Id = canvas.create_oval(370, 370+shadowOffset, 430, 430+shadowOffset, fill=shadowColor, width=0)
    shadow = tc.points
    movePoly(shadow, 0, shadowOffset)
    sw2Id = canvas.create_polygon(*shadow, fill=grayscale(25))

    # draw the coordinator graphic
    tc1Id = canvas.create_oval(370, 370, 430, 430, fill="white", width=0)
    tc2Id = canvas.create_polygon(*tc.points, fill="white", outline="gray", width=2)

    nextUpdate = time.time() + dtGraphics
    while True:
        while time.time() < nextUpdate:
            #time.sleep(dtGraphics/100)
            pass

        nextUpdate = time.time() + dtGraphics

        canvas.delete(tc1Id)
        canvas.delete(tc2Id)
        canvas.delete(sw1Id)
        canvas.delete(sw2Id)

        sw1Id = canvas.create_oval(370, 370+shadowOffset, 430, 430+shadowOffset, fill=shadowColor, width=0)
        shadow = tc.points
        movePoly(shadow, 0, shadowOffset)
        sw2Id = canvas.create_polygon(*shadow, fill=shadowColor)

        tc1Id = canvas.create_oval(370, 370, 430, 430, fill="white", width=0)
        tc2Id = canvas.create_polygon(*tc.points, fill="white")

        window.update()

# The actual execution starts here

if __name__ == "__main__":
    import sys

    # animation window dimension
    height, width = 800, 800

    # animation update rates
    dtState, dtGraphics = 1/1000, 1/60

    try:
        main(height, width, dtState, dtGraphics)
    except KeyboardInterrupt:
        sys.exit()
