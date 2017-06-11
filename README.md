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
street               |  1.201
cooking              |  1.1537
concessionsedit      |  1.1392
something            |  1.1392
brazil               |  1.1392
nutritional content  |  1.1392
kaifeng              |  1.1222
street vendors       |  1.1117
home-cooking         |  1.0459
commercial cooking   |  1.0459

**Top 10 important phrases without clustering**

Key phrases | TF-IDF score
---------------------|--------
hcas             |  0.0449
cancer           |  0.0426
something        |  0.0367
risk             |  0.0349
vitamin          |  0.0266
restaurant       |  0.0244
petrol           |  0.0237
petrol stations  |  0.0237
west             |  0.0237
beef             |  0.0226

## Tests
`python3 tests.py`

## TO-DO

- Add more tests
- Compare clustering algorithms
- More data clearning (to exclude words like `%`)