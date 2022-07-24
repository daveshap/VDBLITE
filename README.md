# Vector Database Lite (VDBLITE)

Vector Database Lite (like SQLITE but for vector search)

To discuss VDBLITE and ask general questions, use https://github.com/daveshap/VDBLITE/discussions 


## Quickstart


1. Install using `pip install vdblite`
2. Run a test with the following code:

```python
import vdblite
from time import time
from uuid import uuid4
import sys
from pprint import pprint as pp


if __name__ == '__main__':
    vdb = vdblite.Vdb()
    dimension = 12    # dimensions of each vector                         
    n = 200    # number of vectors                   
    np.random.seed(1)             
    db_vectors = np.random.random((n, dimension)).astype('float32')
    print(db_vectors[0])
    for vector in db_vectors:
        info = {'vector': vector, 'time': time(), 'uuid': str(uuid4())}
        vdb.add(info)
    vdb.details()
    results = vdb.search(db_vectors[10])
    pp(results)
```

## Class Vdb Methods

### add(payload)

```python
# add a dictionary
info = dict()
vdb.add(info)
# or a list of dictionaries
info = list()
vdb.add(info)
```

Add a an arbitrary number of records to `self.data` (master list of data) of your Vdb object. No checks are performed beyond data type. 

#### payload

Payload must be either a `list` or `dict` variable type. For instance:

```python
info = {
	'time': 123.456789,
	'vector': [0.1, 0.1, 0.1, 0.1, 0.1],
	'uuid': '174657a5-ba76-47a8-a121-5fda05dde560',
	'content': 'lorem ipsum...',
}
```

or

```python
info = [
	{'...'},
	{'...'},
	{'...'},
]
```	

### delete(field, value, firstonly=False)

```python
# delete all records with timestamp at UNIX time of 123.456789
vdb.delete('timestamp', 123.456789, False)
```

Delete record(s) with fields that match a given value

#### field

Specify which element within each record to match for deletion

#### value

Specify value to be matched for deletion

#### firstonly

*Optional.* `False` by default. Will delete all records with `fields` that match `value`. Set to `True` if you only want to delete a single record

### search(vector, field='vector', count=5)

```python
results = vdb.search([1.0, 0.0], 'vector', 5)
```

Search for *n* number of records that are most similar to `vector` (cosine similarity). Specify `field` if searching any other field than *vector*.

#### vector

1-dimensional numpy array to match your query. Performs cosine similarity against all vectors in `self.data`

#### field='vector'

*Optional.* Specify which field contains the *vector* for comparison. Records can contain more than one vector. For instance you may have vectors of different dimensionality, or from different models for different purposes.

#### count=5

*Optional.* Specify number of matches to return.

### bound(field, lower_bound, upper_bound)

```python
results = vdb.bound('time', 123.456789, 987.654321)
```

Return all records with `field` value between `lower_bound` and `upper_bound` e.g. all records with a timestamp between two specific values.

#### field 

Specify which field to compare in all records.

#### lower_bound

Minimum threshold to return.

#### upper_bound

Maximum threshold to return.

### purge()

Delete `self.data` from memory and reinstantiate.

### save(filepath)

```python
vdb.save('my_data.vdb')
```

Save VDB data to file

#### filepath

Relative or absolute filepath of save file

### load(filepath)

```python
vdb = Vdb()
vdb.load('my_data.vdb')
```

Load saved VDB data into memory

#### filepath

Relative or absolute filepath of save file
