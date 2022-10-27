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

# Mathematics
import math

class Statistics():
    """
    Computes various statistics
    """
    @staticmethod
    def computeMeanTimeBetweenFailures(values):
        """
        Computes mean time between failures
        How many seconds the truck was online
        """
        gap = False
        prevValue = None
        prevTimestamp = None
        start = True
        gapStart = None
        stats = []
        for (timestamp, value) in values:
            if timestamp == None or value == None:
                continue;
            if start:
                start = False
                prevTimestamp = timestamp
                prevValue = value
                if prevValue == math.inf:
                    gapStart = timestamp
                    gap = True
                continue 
            if (prevValue != math.inf and value == math.inf):
                if not gap:
                    prevTimestamp = timestamp
                    gapStart = timestamp
                    gap = True
                prevValue = value
            if (prevValue == math.inf and value != math.inf):
                if gap:
                    gapValue = timestamp - gapStart
                    gap = False
                    stats.append(gapValue)
                prevValue = value
        print(stats)
        return stats
