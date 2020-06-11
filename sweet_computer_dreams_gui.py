from tkinter import *


class tkiner_program():
    def __init__(self):
        self.interface = Tk()
        self.center_window(1200, 600)

        self.interface.title("Sweet Computer Dreams Graphics User Interface") 

        lbl = Label(window, text="Hello")

        lbl.grid(column=0, row=0)

        btn = Button(interface, text="Click Me", command=click_to_start_timer)
        btn.grid(column=5, row=3)


        self.interface.mainloop()

    def center_window(self,w=300, h=200):
        # get screen width and height
        ws = self.interface.winfo_screenwidth()
        hs = self.interface.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.interface.geometry('%dx%d+%d+%d' % (w, h, x, y))


    """
    def click_to_start_timer():
        .configure(text="Button was clicked !!")
    """




def main():
    initalize_tkiner_windows()

# Start the program
main()