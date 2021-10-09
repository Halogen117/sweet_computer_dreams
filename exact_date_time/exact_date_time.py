import tkinter
import datetime
class exact_date_time:
    def __init__(self, exact_date, exact_time):
        print("Initiailzing exact_date_time class")
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.combined_exact_date_time = datetime.datetime.strptime(exact_date+' '+exact_time,'%d/%m/%Y %H:%M:%S')
    def center_window(self,window, w=300, h=200):
        # get screen width and height
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def destroy_gui(self,master):
        master.destroy()

    def analyze_time_format(self):

        # To be calculated to seconds to plot forth the date
        # Convert date/time to date/time format

        #new date - current date
        date_diff = self.combined_exact_date_time - datetime.datetime.today()
        # Possible error scenarios
        #new date > old date but old time > old date
        # empty new date and empty new time
    # Utilize with the gui for future performances. For now need to optimize for a standerdized date
    '''
    def different_time_format(self):
        hour_define = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        minute_define = []

        for minute in range(0,61):
            minute_define.append(minute)
        
        master = tkinter.Tk()
        self.center_window(master,1200,600)
        master.title("Set Timer")
        hour_option = tkinter.OptionMenu(master,tkinter.StringVar(), *hour_define, command=lambda:self.get_hour_value())
        minute_option = tkinter.OptionMenu(master,tkinter.StringVar(), *minute_define, command=lambda:self.get_minute_value())
        second_option = tkinter.OptionMenu(master,tkinter.StringVar(), *minute_define, command=lambda:self.get_second_value())
        start = tkinter.Button(master, text='Start Timer!', command=lambda:self.destroy_gui(master))
        
        hour_option.grid(row=0, column=0)
        minute_option.grid(row=0, column=1)
        second_option.grid(row=0, column=2)
        start.grid(row=1, column=1)
        master.mainloop()
    '''
    def get_year_value(self, selection):
        self.year = selection

    def get_month_value(self, selection):
        self.month = selection

    def get_day_value(self, selection):
        self.day = selection

    def get_hour_value(self, selection):
        self.hour = selection

    def get_minute_value(self, selection):
        self.minute = selection

    def get_second_value(self, selection):
        self.second = selection
    '''
    def different_date_format(self):
        year_define = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        day_define = []

        for day in range(0,32):
            day_define.append(day)
        
        master = tkinter.Tk()
        self.center_window(master,1200,600)
        master.title("Set Timer")
        year_option = tkinter.OptionMenu(master,tkinter.StringVar(), *year_define, command=lambda:self.get_year_value())
        month_option = tkinter.OptionMenu(master,tkinter.StringVar(), *year_define, command=lambda:self.get_month_value())
        day_option = tkinter.OptionMenu(master,tkinter.StringVar(), *day_define, command=lambda:self.get_day_value())
        start = tkinter.Button(master, text='Start Timer!', command=lambda:self.destroy_gui(master))
        
        year_option.grid(row=0, column=0)
        month_option.grid(row=0, column=1)
        day_option.grid(row=0, column=2)
        start.grid(row=1, column=1)
        master.mainloop()

        def compile_date(self):
            if self.exact_date is None:
                print("Taking today's date")
                today_date = datetime.date.today()
                return today_date.year, today_date.month, today_date.day


            return self.year, self.month, self.day

        def compile_time(self):
            if self.exact_time is None:
                today_time = datetime.datetime.now()
                return today_time.hour, today_time.minute, today_time.second
    
    '''

