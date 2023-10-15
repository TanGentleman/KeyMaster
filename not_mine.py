# The code below demonstrates that there is a way to simulate keys being pressed to write a text without having to create a single line for each letter that the script would have to type.

# In addition to that the provided solution allows to execute code placed in the same script after the code for automated typing which feature is used to show the automated keyboard input in a typing speed test GUI:

import pynput
import random 
import threading
import time

txt = "pynput is typing like a human"
#txt = "abc" 

class Sim_keyb_typing(threading.Thread):
    def __init__(self, text, 
                 strt_delay=1.5, 
                 dct_delays={('a','i'):0.15}, 
                 delayrange=(0.1, 0.3) ):
        threading.Thread.__init__(self)

        self.text       = text
        self.strt_delay = strt_delay
        self.last_char  = " "
        self.dct_delays = dct_delays
        self.delayrange = delayrange

        self.ppkbC = pynput.keyboard.Controller()

    def run(self):
        time.sleep(self.strt_delay)
        for char in self.text:
            delay = self.dct_delays.get( 
                (self.last_char, char), random.uniform(*self.delayrange) )
            time.sleep(delay)
            self.ppkbC.type(char)
            self.last_char = char

# Let's wait 1.5 seconds and then start typing: 
skt = Sim_keyb_typing(txt)
skt.start()
# Wait for Sim_keyb_typing(txt) to finish
#skt.join()

# ======================================================================
import tkinter
import time
import threading
import random
import string

class simpleTypeSpeedGUI: # creates tkinter GUI mainloop

    def __init__(self, txt):
        self.root = tkinter.Tk()
        self.root.title("Type Speed Test (starts on first keypress)")
        self.root.geometry("1600x400")

        self.text_lines = txt.split("\n")
        self.text_line = random.choice(self.text_lines)
        self.len_text_line = len(self.text_line)

        # Label showing text to type:
        self.sample_label = tkinter.Label(self.root, text=self.text_line, font=("Helvetica", 14))
        self.sample_label.grid( row=0, column=1, columnspan=2, padx=15, pady=15, sticky='w')

        # Text box receiving typing input: 
        self.input_textbox = tkinter.Entry(self.root, width=120, font=("Helvetica", 14))
        self.input_textbox.grid(row=1, column=1, columnspan=2, padx=15, pady=15)
        # Registering callback function for text box keyboard input keypress
        self.input_textbox.bind("<KeyRelease>", self.on_key_up) 
        # The reason for          KeyRelease  is to have updated widget content in the callback function
        self.input_textbox.focus()

        # Label showing typing speed: 
        self.speed_label = tkinter.Label(self.root, text="Typing speed: \n---- \n---- \n---- \n---- ", font=("Helvetica", 12))
        self.speed_label.grid(row=2, column=1, columnspan=2, padx=5, pady=10)

        # Button for restart/reset of typing: 
        self.reset_button = tkinter.Button(self.root, text="Reset", command=self.reset, font=("Helvetica", 18))
        self.reset_button.grid(row=3, column=1, columnspan=2, padx=15, pady=15)

        # Standard value for average number of characters in a word 
        self.std_char_per_word = 5
        # used to calculate words per minute from typing speed in chars/min

        # initialisation of code flow control values: 
        self.start_time     = None
        self.end_time       = None
        self.printable = string.printable[:-5]

        self.root.mainloop()

    def on_key_up(self, event):
        # processing on key release because on key press results
        # in the widget content are not yet updated with the key char. 
        if event.keycode == 9: # pressed Escape => EXIT
            print("\nEscape-EXIT")
            self.root.destroy()
            return # <- required because root.destroy() doesn't block 
                   # execution of further code which then runs into 
                   # trouble as .destroy() makes widgets not available

        if self.start_time is None:
            self.start_time = time.perf_counter()

        input_textbox = self.input_textbox.get()
       
        # print(f'{event.keycode=} => "{event.char=}" ')

        if input_textbox == self.text_line:
            self.running = False
            self.input_textbox.config(fg="green")
            self.end_time = time.perf_counter()
        else: 
            if self.text_line.startswith(input_textbox):
                self.input_textbox.config(fg="black")
            else:
                self.input_textbox.config(fg="red")

        self.show_typespeed()

    def show_typespeed(self):
        curr_time = time.perf_counter()
            
        if   self.start_time is not None and self.end_time is not None:  
            time_diff = self.end_time - self.start_time
        elif self.start_time is not None and self.end_time is None: # and self.end_time is None  
            time_diff = curr_time - self.start_time
        elif self.start_time is None and self.end_time is None: 
            self.speed_label.config(text="Speed: \n---- CPS\n---- CPM\n---- WPS\n---- WPS")
            return
        cps = self.len_text_line / time_diff
        cpm = cps * 60.0
        wps = cps / self.std_char_per_word
        wpm = wps * 60.0
        self.speed_label.config(text=f"Speed: \n{cps:5.2f} CPS\n{cpm:5.2f} CPM\n{wps:5.2f} WPS\n{wpm:5.2f} WPM")

    def reset(self):
        self.start_time = None
        self.end_time   = None
        self.text_line = random.choice(self.text_lines)
        self.len_text_line = len(self.text_line)
        self.sample_label.config(text=self.text_line)
        self.input_textbox.delete(0, tkinter.END)
        self.show_typespeed()

sTSG = simpleTypeSpeedGUI(txt)