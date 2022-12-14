#!/usr/bin/python3

# Copyright (C) 2022 Micromine
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Timing
import time
# Import tkinter UI
from tkinter import *
# Math utils
import math
# Threading
import threading
# Plotting
import matplotlib.pyplot as plt
# Statistics
import utils
from utils import statistics
# Logging functionality
import logging
# Import subprocess stuff
import subprocess
# Font 
import tkinter.font as font

__REFRESH_RATE__ = 1

class Main():
    """
    Main application window
    """

    def __init__(self, storage, lock):
        """
        Initializes the class
        """
        self.storage = storage
        self.lock = lock
        self.keys = self.storage.get_all_keys();
        self.labels = {}
        self._MAX_COLS = 7

    def update(self, window = None):
        while True:
            logging.debug("Updating the UI")
            for key in self.keys:
                btn = self.labels[key]
                self.lock.acquire()
                last_value = self.storage.get_last(key)
                self.lock.release()
                if last_value[1] != math.inf:
                    try:
                        btn["text"] = "Online " + str(round(last_value[1], 2))
                    except:
                        pass
                    btn["bg"] = "#00FF00"
                else:
                    btn["text"] = "Offline"
                    btn["bg"] = "#FF0000"
            
            time.sleep(__REFRESH_RATE__)
            self.window.update()

    def showMTBFGraph(self, key):
        self.lock.acquire();
        values = self.storage.get_all(key)
        self.lock.release();
        logging.debug(values)
        mtbf_data = statistics.Statistics.computeMeanTimeBetweenFailures(values)
        plt.hist(mtbf_data)
        plt.show()

    def runVNCViewer(self, key):
        try:
            subprocess.run(["config/vncviewer.exe", key])
        except:
            pass

    def show(self):
        self.window = Tk()
        self.window.state("zoomed")
        self.window.title("Ping statistics")
        cpos = 20;
        row_index = 1
        col_index = 0
        num_columns = 6;
        num_elems = 3;
        start = True;
        myfont = font.Font(size=7)
        for key in self.keys:
            if start:
                lbl = Label(self.window, text = "Host")
                lbl.grid(row = 0, column = col_index % (num_columns*num_elems))
                lbl["font"] = myfont
                lbl = Label(self.window, text = "Status")
                lbl["font"] = myfont
                lbl.grid(row = 0, column = (col_index + 1) % (num_columns*num_elems))
                lbl = Label(self.window, text = "VNC")
                lbl["font"] = myfont
                lbl.grid(row = 0, column = (col_index + 2) % (num_columns*num_elems))
                
            hostlbl = Label(self.window, text = key)
            hostlbl["font"] = myfont
            hostlbl.grid(row=row_index, column=col_index % (num_columns*num_elems))

            if self.storage.get_last(key)[1] != math.inf:
                btn = Button(self.window, bg='#00FF00', text = "Online " + str(round(self.storage.get_last(key)[1], 2)), command = lambda key=key: self.showMTBFGraph(key))
                btn.grid(row = row_index, column = (col_index + 1) % (num_columns*num_elems))
                btn["font"] = myfont
                self.labels[key] = btn
            else:
                btn = Button(self.window, bg='#FF0000', text = "Offline", command = lambda key=key: self.showMTBFGraph(key))
                btn.grid(row = row_index, column = (col_index + 1) % (num_columns*num_elems))
                btn["font"] = myfont
                self.labels[key] = btn

            btn = Button(self.window, text = "Conn.", command = lambda key=key: self.runVNCViewer(key))
            btn.grid(row = row_index, column = (col_index + 2) % (num_columns*num_elems))
            btn["font"] = myfont
            
            if row_index > 1:
                start = False
            col_index += num_elems
            if col_index % (num_columns*num_elems) == 0 and col_index != 0:
                row_index += 1

        redraw_thread = threading.Thread(target = self.update, args = (), daemon = True);
        redraw_thread.start();
        self.window.update()
        self.window.mainloop()
        
