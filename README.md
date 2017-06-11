# yuki4i2x

![alt text](https://raw.githubusercontent.com/yukiegosapporo/keyword_extractor/master/data/structure.png)

## Quick start

```cd keyword_extractor```
```python main.py --use-cluster True --top-n 10```
This will perform:
- basic data clearning (to lower case and lemma TODO)
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

## Challenges

The main idea is to run TF-IDF for important words/phrases but naive
implementation might not give optimal solutions because **some documents cover
similar topics (like food)**.  
So first doc2vec computes vector representation of each document so similar
documents are joined together.  
Now we have the preprocessed and clustered documents, TF-IDF should perform a
better keyword extraction.  

## Tests
`python3 tests.py`

## TO-DO

- Add more tests
- Compare clustering algorithms
- More data clearning (to exclude words like `%`)