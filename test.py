import faiss
import pickle
import numpy as np
from time import time
from uuid import uuid4
import sys
from pprint import pprint as pp



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
    
    def initialize(self, field='vector', clusters=5):
        dimension = len(self.data[0][field])
        nlist = clusters  # number of clusters TODO this should be dynamic
        quantiser = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIVFFlat(quantiser, dimension, nlist, faiss.METRIC_L2)
        vectors = [i[field] for i in self.data]
        self.index.train(vectors)
        self.index.add(vectors)
        print('Index is trained:', self.index.is_trained)

    def index_search(self, vector, count=5):
        distances, indices = self.index.search(list(vector), count)
        result = list()
        for idx in indices[0]:
            result.append self.data[idx]
        return result        
    
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

    def save_index(self, filepath):
        faiss.write_index(self.index, filepath)

    def load(self, filepath):
        with open(filepath, 'wb') as infile:
            self.data = pickle.load(infile)

    def load_index(self, filepath):
        self.index = faiss.read_index(filepath)  # load the index

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