# Done
1. Profiling the memory usage of a python script

https://github.com/plasma-umass/scalene

https://github.com/bloomberg/memray

find the entry point of the huge memory usage at 
'FedSimModel.py:165'
'filter_to_topk_dataset_() SimModel.py:236'

it will make a cross join to the whole dataset
for example, if the dataset shape is [98735, 77], it will make a [98735*k, 77] matrix
where k is the number of topk

consider to use more efficient way to do store the data
for example, use a dict to store the data, and use a list to store the key
then we can use the key to get the data from the dict
second, we can use a list to store the data, and use a list to store the index
then we can use the index to get the data from the list

don't know if it is possible to use the sparse matrix to store the data, or will it impact the training speed

may involve the data transmittion between the GPU and CPU, which will be very slow

maybe we can use the sparse matrix to store the data, and use the index to get the data from the sparse matrix
or we can pre-process the data, and store the data into the GPU when training.

# TODO
1. Find a new data structure to store the data
maybe find some paper to support your finding