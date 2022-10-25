#!/usr/bin/python3

# Copyright (C) 2019 Micromine
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

__REFRESH_RATE__ = 1

class Main():
    """
    Main application window
    """

    def __init__(self, storage):
        """
        Initializes the class
        """
        self.storage = storage
        self.keys = self.storage.get_all_keys();
        self.labels = {}
        self._MAX_COLS = 5

    def update(self):
        for key in self.keys:
            statuslbl = self.labels[key]
            if self.storage.get_last(key)[1] != math.inf:
                statuslbl["text"] = "Online " + str(round(self.storage.get_last(key)[1], 2))
                statuslbl["bg"] = "#00FF00"
            else:
                statuslbl["text"] = "Offline"
                statuslbl["bg"] = "#FF0000"
        time.sleep(__REFRESH_RATE__)

    def showMTBFGraph(self, key):
        values = self.storage.get_all(key)
        mtbf_data = statistics.Statistics.computeMeanTimeBetweenFailures(values)
        plt.hist(mtbf_data)
        plt.show()
    def show(self):
        window = Tk()
        window.state("zoomed")
        window.title("Ping statistics")
        cpos = 20;
        row_index = 1
        col_index = 0
        start = True;
        for key in self.keys:
            if start:
                lbl = Label(window, text = "Host")
                lbl.grid(row = 0, column = col_index % 15)
                lbl = Label(window, text = "Show MTBF plot")
                lbl.grid(row = 0, column = (col_index + 1) % 15)
                lbl = Label(window, text = "Status")
                lbl.grid(row = 0, column = (col_index + 2) % 15)
            hostlbl = Label(window, text = key)
            hostlbl.grid(row=row_index, column=col_index % 15)
            btn = Button(window, text = "Show MTBF distribution", command = lambda : self.showMTBFGraph(key))
            btn.grid(row=row_index, column=(col_index + 1) % 15)
            if self.storage.get_last(key)[1] != math.inf:
                statuslbl = Label(window, bg='#00FF00', text = "Online " + str(round(self.storage.get_last(key)[1], 2)))
                statuslbl.grid(row = row_index, column = (col_index + 2) % 15)
                self.labels[key] = statuslbl
            else:
                statuslbl = Label(window, bg='#FF0000', text = "Offline")
                statuslbl.grid(row = row_index, column = (col_index + 2) % 15)
                self.labels[key] = statuslbl
            if row_index > 1:
                start = False
            col_index += 3
            if col_index % 15 == 0 and col_index != 0:
                row_index += 1
        redraw_thread = threading.Thread(target = self.update, args = (self), daemon = True);
        redraw_thread.start();
        window.update()
        window.mainloop()
        
