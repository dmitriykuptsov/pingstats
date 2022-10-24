class CyclicStorage():
    def __init__(self, max_records = 1000):
        self.max_records = max_records;
        self.storage = {}
        self.counters = {}
    def put(self, key, value, timestamp):
        if key not in self.storage.keys():
            self.storage[key] = [None] * self.max_records;
            self.counters[key] = 0;
        self.storage[key][self.counters[key] % self.max_records] = (timestamp, value)
        self.counters[key] = self.counters[key] % self.max_records;
    def set_counter(self, key, counter):
        self.counters[key] = counter;
    def get_all(self, key):
        return self.storage[key];
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
