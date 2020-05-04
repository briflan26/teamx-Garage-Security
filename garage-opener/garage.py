"""
THIS FILE WILL CONTAIN ALL THE CODE TO OPEN AND CLOSE THE GARAGE
"""
from appJar import gui

closed = False
open = True
state = closed


def open_g():
    global state
    if state == closed:
        app = gui()
        print("Opening")
        app.setFont(size=24) #, family="Sans Serif")
        app.setTitle("Opening Garage Door")
        app.addLabel("l1", "Opening Garage")
        app.addImage("opening", "open.gif")
        app.zoomImage("opening", -1)
        app.setImageSize("opening", 300, 300)
        app.setSize(400, 400)
        app.setBg("green")
        print("Launching")
        app.go()
        state = open
    return


def close_g():
    global state
    if state == open:
        app = gui()
        print("Closing")
        app.setFont(size=24) #, family="Sans Serif")
        app.setTitle("Closing Garage Door")
        app.addLabel("l1", "Closing Garage")
        app.addImage("closing", "closed.gif")
        app.setSize(400, 400)
        app.setBg("red")
        app.go()
        state = closed
    return
