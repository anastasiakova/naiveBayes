from Tkinter import *
import tkFileDialog

from buildModel import *

def model():
    global classifier
    classifier = buildTheModel(path, binsNumber)

def browseButtonOpen():
    filename = tkFileDialog.askdirectory()
    path.set(filename)

def initWindow(root):
    root.title("Naive Bayes Classifier")
# browse
    global path
    path = StringVar()
    folderPathEntry = Entry(root,textvariable=path)
    folderPathEntry.grid(row=0, column=1)

    browseButton = Button(text="Browse", command=browseButtonOpen)
    browseButton.grid(row=0, column=2)

    browseLbl = StringVar()
    browseLbl.set("Directory Path")
    folderPathLbl = Label(master=root, textvariable=browseLbl)
    folderPathLbl.grid(row=0, column=0)

#bins
    global binsNumber
    binsNumber = StringVar()
    binsEntry = Entry(root,textvariable=binsNumber)
    binsEntry.grid(row=1, column=1)
    binsLblString = StringVar()
    binsLblString.set("Discretization Bins")
    binsLbl = Label(master=root,textvariable=binsLblString)
    binsLbl.grid(row=1, column=0)

#buttons
    build = Button(text="Build", command = model)
    build.grid(row=2, column=1)

    classify = Button(text="Classify", command = lambda: classifier.classify(path))
    classify.grid(row=3, column=1)


root = Tk()
initWindow(root)
mainloop()

