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

class CyclicStorage():
    def __init__(self, max_records = 1000):
        self.max_records = max_records;
        self.storage = {}
        self.counters = {}
    def put(self, key, value, timestamp):
        if key not in self.storage.keys():
            self.storage[key] = [None] * int(self.max_records);
            self.counters[key] = 0;
        self.storage[key][self.counters[key] % self.max_records] = (timestamp, value)
        self.counters[key] = self.counters[key] % self.max_records;
    def set_counter(self, key, counter):
        self.counters[key] = counter;
    def get_counter(self, key):
        return self.counters[key]
    def get_max_records(self):
        return self.max_records
    def get_all(self, key):
        arr = self.storage[key];
        start = self.counters[key]
        output = []
        for i in range(start, start + self.max_records):
            j = i % self.max_records
            output.append(arr[j])
        return output
    def get_slice(self, key, start, end):
        if start < 0 or start > end:
            raise Exception("Invalid index")
        if end > self.max_records:
            raise Exception("Invalid index")
        return self.storage[key][start:end];
    def get_last(self, key):
        return self.storage[key][self.counters[key] % self.max_records]
    def dump_to_file(self, file):
        fh = open(file, "w+")
        fh.writeline(self.max_records)
        for key in self.storage.keys():
            fh.writeline(self.counters[key])
            for i in range(0, self.max_records):
                fh.writeline("%s %s %s" % (self.storage[key][i][0], self.storage[key][i][1]))
        fh.flush();
        fh.close();
    @staticmethod
    def load_from_file(self, file):
        fh = open(file, "r")
        records = fh.readlines()
        max_records = int(records[0])
        storage = CyclicStorage(max_records);
        max_keys = (len(records) - 1) / (max_records + 1);
        for i in range(0, max_keys):
            key = records[i*(max_records + 1)].split(" ")[0]
            counter = int(records[i*(max_records + 1)].split(" ")[1])
            storage.set_counter(key, counter)
            for j in range(0, max_records): 
                parts = records[i*(max_records + 1) + j + 2].split(" ")
                storage.put(key, parts[1], parts[0])
        return storage
