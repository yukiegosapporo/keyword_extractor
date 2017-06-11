# yuki4i2x

![alt text](https://raw.githubusercontent.com/yukiegosapporo/keyword_extractor/master/images/structure.png)

## Quick start

```cd keyword_extractor```  
```python main.py --use-cluster True --top-n 10```

## How does this work

The main idea is to run TF-IDF for important words/phrases but naive
implementation might not give optimal solutions because **some documents cover
similar topics (like food)**.  
So first doc2vec computes vector representation of each document so similar
documents are joined together.  
Now we have the preprocessed and clustered documents, TF-IDF should perform a
better keyword extraction.  

- basic data clearning (to lower case and lemmatization)
- doc2vector to obtain vector representations for documents (set
`--use-cluster` to `False` to skip this)
- AffinityPropagation to cluster documents
- concatenattion of similar documents
- TF-IDF to obtain important words/phrases
- save top 10 (change `--top-n N` to save top N) most important ones to csv

## Install

```git clone https://github.com/yukiegosapporo/keyword_extractor.git```  
```cd keyword_extractor```  
```pip install -r requirements.txt```   


## Analysis

**Top 10 important phrases with clustering**

Key phrases | TF-IDF score
---------------------|--------
mcdonald     |  0.038400000000000004
mcdonald 's  |  0.033299999999999996
york         |  0.0308
press        |  0.0305
obesity      |  0.029099999999999997
new york     |  0.0277
fast         |  0.0268
sugar        |  0.026099999999999998
company      |  0.0256
study        |  0.0255

**Top 10 important phrases without clustering**

Key phrases | TF-IDF score
---------------------|--------
international food imports  |  1.961
dietary problems            |  1.961
nutrition                   |  1.635
food                        |  1.6154
cooking                     |  1.6096
%                           |  1.4789
street                      |  1.4233
something                   |  1.3397
taste                       |  1.3393
kaifeng                     |  1.3100999999999998

## Tests
`python3 tests.py`

## TO-DO

- Add more tests
- Compare clustering algorithms
- More data clearning (to exclude words like **%** and combine **mcdonald**
and **mcdonald 's**)