"""
THIS FILE WILL CONTAIN ALL THE CODE TO OPEN AND CLOSE THE GARAGE
"""
from appJar import gui
app = gui()


def open_g():
    print("Opening")
    app.stop();
    app.addLabelEntry("title", "Opening Garage Door")
    app.setLabelBg("title", "green")
    app.addButtons(["Dismiss"], press)
    app.go()


def close_g():
    print("Closing")
    app.stop()
    app.addLabelEntry("title", "Closing Garage Door")
    app.setLabelBg("title", "red")
    app.addButtons(["Dismiss"], press)
    app.go()


def press(button):
    if button == "Dismiss":
        app.stop()
    else:
        return
