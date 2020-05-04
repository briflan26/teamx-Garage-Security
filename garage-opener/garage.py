"""
THIS FILE WILL CONTAIN ALL THE CODE TO OPEN AND CLOSE THE GARAGE
"""
from time import sleep

from appJar import gui

closed = False
opened = True

state = closed
app = None





def open_g():
    global state
    global app
    if state == closed:
        app = gui(showIcon=False)
        print("Opening")
        app.setFont(size=24)
        app.setTitle("Opening Garage Door")
        app.addLabel("l1", "Opening Garage")
        app.addImage("opening", "open.gif")
        app.zoomImage("opening", -1)
        app.setImageSize("opening", 300, 300)
        app.setSize(400, 400)
        app.setBg("green")
        app.setOnTop(stay=True)
        print("Launching")
        app.go()
        state = opened
    return


def close_g():
    global state
    global app
    if state == opened:
        app = gui(showIcon=False)
        print("Closing")
        app.setFont(size=24)
        app.setTitle("Closing Garage Door")
        app.addLabel("l1", "Closing Garage")
        app.addImage("closing", "closed.gif")
        app.setSize(400, 400)
        app.setBg("red")
        app.setOnTop(stay=True)

        print("Launching")
        app.go()
        state = closed
    return
