# Installation

`pip install fito`


# Functionality

Fito is a package that works around the concept of `Operations` and `DataStores`.

The simplest way of thinking it is that a subclass of `Operation` defines
a function, and an instance defines that function being also binded 
to it's arguments. 

If the types of the function inputs are **json-serializable**, 
then the `Operation` is as well. 
Not only that, but operations are also **hashable**.

That leads us to the `DataStore`, whose capability is to index an `Operation`.
There are two implementations, one that uses the file system and 
anotherone that uses [MongoDB](https://www.mongodb.com/).

Extra features:
* `as_operation` Decorator that turns any function into a subclass of `Operation`
* `DataStore.autosaved`: Decorator to turn automatic caching on any function. 
Creates an operation out of the function and the data store is used for caching the results. 
* Both decorators can be used for functions, instance and class methods.

A small example is worth
```
from fito.data_store.file import FileDataStore
ds = FileDataStore('test') # can be reeplaced by MongoHashMap

@ds.cache()
def f(x, y=1):
    print "executed"
    return x + y
```

An example output would be
```
In [26]: f(1)
executed
Out[26]: 2

In [27]: f(1)
Out[27]: 2
In [30]: ds.clean()

In [31]: f(1)
executed
Out[31]: 3
```