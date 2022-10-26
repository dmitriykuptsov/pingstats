#!/usr/bin/python

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

class Misc():
    """
    Class stores various helper methods
    """
    @staticmethod
    def load_hosts(file):
        """
        Loads hosts from file
        """
        fh = open(file, "r")
        hosts = []
        lines = fh.readlines()
        for line in lines:
            hosts.append(line.strip())
        return hosts
    @staticmethod
    def load_config(file):
        """
        Loads configurations from file
        """
        fh = open(file, "r")
        config = {}
        lines = fh.readlines()
        for line in lines:
            cfg = line.strip().split(":")
            config[cfg[0]] = cfg[1]
        return config