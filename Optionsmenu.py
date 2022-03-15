import tkinter as tk
import threading

thr = None


def openMenu(keymap, camContainer):
    global thr
    if thr is not None and thr.isAlive():
        return

    namemap = {}
    for v in keymap.values():
        namemap[v.__name__] = v

    thr = threading.Thread(target = tkPopup,
                           args = (namemap, camContainer)
                           )
    thr.start()


def tkPopup(namemap, camContainer):
    win = tk.Tk()
    win.minsize(300, 300)

    def setoptiontext(value):
        entry.delete(1.0, "end")
        inserttext = namemap[value].defaults
        entry.insert(1.0, dictprinter(inserttext))

    things = list(namemap.keys())
    choice = tk.StringVar()
    choice.set(things[0])
    w = tk.OptionMenu(win, choice, *things, command = setoptiontext)
    w.grid(row = 0, column = 0)

    entry = tk.Text(win, width = 40, height = 15)
    entry.grid(row = 1, column = 0)

    buttonFrame = tk.Frame(win)
    buttonFrame.grid(row = 2, column = 0)

    cancel = tk.Button(buttonFrame, text = "Cancel", command = win.destroy)
    cancel.pack(side = tk.LEFT)

    def update():
        from numpy import array
        #print(entry.get("1.0", "end"))
        options = eval(entry.get("1.0", "end")) # Eww, Sorry about this
        camContainer.changeCam(namemap[choice.get()].Camera, **options)
        win.destroy()

    go = tk.Button(buttonFrame, text = "Go", command = update)
    go.pack(side = tk.LEFT)

    setoptiontext(choice.get())
    tk.mainloop()


def dictprinter(dic):
    out = "{\n"
    for k, v in dic.items():
        out += repr(k) + " : " + repr(v) + ",\n"
    out += "}"
    return out

