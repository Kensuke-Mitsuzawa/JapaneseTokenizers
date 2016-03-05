# What's this?

This is simple wrapper for Japanese Tokenizers(A.K.A Morphology Splitter)

This repository aims to call Tokenizer and split into tokens in one line.

If you find any bugs, please report them to github issues. Or any pull requests are welcomed!

# Features

* put sentence and get set of tokens
* filter some tokens with your Part-of-Speech condition or stopwords
* be able to add extension dictionary like mecab-neologd dictionary
* be bale to define your original dictionary. And this dictionary forces mecab to make it one token
 
# Setting up

## Python version

This package works under both of python2x and python3x.

## MeCab system

See [here](https://github.com/jordwest/mecab-docs-en) to install MeCab system.

## Mecab Neologd dictionary

Mecab-neologd dictionary is a dictionary-extension based on ipadic-dictionary, which is basic dictionary of Mecab.

With, Mecab-neologd dictionary, you're able to new-coming words make one token.

Here, new-coming words is suche like, movie actor name or company name.....

See here[https://github.com/neologd/mecab-ipadic-neologd] and install mecab-neologd dictionary.


## python library

execute following command

```
python install_python_dependencies.py
```

This command automatically install all libraries that this package depends on.

## install

```
[sudo] python setup.py install
```


# example usage

See `examples/` to use.

