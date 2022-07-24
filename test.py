import pickle
import numpy as np
from time import time
from uuid import uuid4
import sys
from pprint import pprint as pp
from multiprocessing import Pool


class Vdb():
    def __init__(self):
        self.data = list()
    
    def add(self, payload):  # payload is a DICT or LIST
        if isinstance(payload, dict):   # payload is a dict, so append
            self.data.append(payload)  # uuid could be in payload :) 
        elif isinstance(payload, list):     # payload is a list, so concatenate lists
            self.data = self.data + payload
    
    def delete(self, field, value, firstonly=False):
        for i in self.data:
            try:
                if i[field] == value:  # if field == 'timestamp' then value might be 1657225709.8192494
                    self.data.remove(i)
                    if firstonly:
                        return
            except:
                continue
    
    def search(self, vector, field='vector', count=5):
        results = list()
        for i in self.data:
            try:
                score = np.dot(i[field], vector)
            except Exception as oops:
                print(oops)
                continue
            info = i
            info['score'] = score
            results.append(info)
        ordered = sorted(results, key=lambda d: d['score'], reverse=True)
        try:
            ordered = ordered[0:count]
            return ordered
        except:
            return ordered
    
    def bound(self, field, lower_bound, upper_bound):
        # return all results that have a field with a value between two bounds, i.e. all items between two timestamps
        results = list()
        for i in self.data:
            try:
                if i[field] >= lower_bound and i[field] <= upper_bound:
                    results.append(i)
            except:
                continue
        return results
    
    def purge(self):
        del self.data
        self.data = list()
    
    def save(self, filepath):
        with open(filepath, 'wb') as outfile:
            pickle.dump(self.data, outfile)

    def load(self, filepath):
        with open(filepath, 'wb') as infile:
            self.data = pickle.load(infile)

    def details(self):
        print('DB elements #:', len(self.data))
        print('DB size in memory:', sys.getsizeof(self.data), 'bytes')



if __name__ == '__main__':
    print('instantiating arrays')
    vdb = Vdb()
    dimension = 128    # dimensions of each vector                         
    count = 10000000          # number of vectors                   
    np.random.seed(1)             
    #db_vectors = np.random.random((n, dimension)).astype('float32')
    print('loading up the database')
    for n in range(0, count):
        vector = np.random.random(dimension).astype('float16')
        info = {'vector': vector, 'time': time(), 'uuid': str(uuid4())}
        vdb.add(info)
        if n % 50000 == 0:
            print(n)
    vdb.details()
    print('starting search')
    start = time()
    results = vdb.search(np.random.random(dimension).astype('float16'))
    end = time()
    print('regular search time (s):', end-start)
    #pp(results)
    exit(0)
    #start = time()
    #results = vdb.new_search(db_vectors[10])
    #end = time()
    #print('new search time (s):', end-start)