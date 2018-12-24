[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)[![Build Status](https://travis-ci.org/Kensuke-Mitsuzawa/JapaneseTokenizers.svg?branch=master)](https://travis-ci.org/Kensuke-Mitsuzawa/JapaneseTokenizers)


# What's this?

This is simple python-wrapper for Japanese Tokenizers(A.K.A Tokenizer)

This project aims to call tokenizers and split a sentence into tokens as easy as possible.

And, this project supports various Tokenization tools common interface. Thus, it's easy to compare output from various tokenizers.

This project is available also in [Github](https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers).  

If you find any bugs, please report them to github issues. Or any pull requests are welcomed!

# Requirements

- Python 2.7
- Python 3.x
    - checked in 3.5, 3.6, 3.7  


# Features

* simple/common interface among various tokenizers
* simple/common interface for filtering with stopwords or Part-of-Speech condition 
* simple interface to add user-dictionary(mecab only)

## Supported Tokenizers

### Mecab

[Mecab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html?sess=3f6a4f9896295ef2480fa2482de521f6) is open source tokenizer system for various language(if you have dictionary for it)

See [english documentation](https://github.com/jordwest/mecab-docs-en) for detail

### Juman

[Juman](http://nlp.ist.i.kyoto-u.ac.jp/EN/index.php?JUMAN) is a tokenizer system developed by Kurohashi laboratory, Kyoto University, Japan.

Juman is strong for ambiguous writing style in Japanese, and is strong for new-comming words thanks to Web based huge dictionary.
 
And, Juman tells you semantic meaning of words.

### Juman++

[Juman++](http://nlp.ist.i.kyoto-u.ac.jp/EN/index.php?JUMAN++) is a tokenizer system developed by Kurohashi laboratory, Kyoto University, Japan.

Juman++ is succeeding system of Juman. It adopts RNN model for tokenization.

Juman++ is strong for ambigious writing style in Japanese, and is strong for new-comming words thanks to Web based huge dictionary.
 
And, Juman tells you semantic meaning of words.

Note: New Juman++ dev-version(later than 2.x) is available at [Github](https://github.com/ku-nlp/jumanpp)


### Kytea

[Kytea](http://www.phontron.com/kytea/) is tokenizer tool developped by Graham Neubig.

Kytea has a different algorithm from one of Mecab or Juman. 

 
# Setting up

## Tokenizers auto-install

```
make install
```

### mecab-neologd dictionary auto-install

```
make install_neologd
```

## Tokenizers manual-install

### MeCab

See [here](https://github.com/jordwest/mecab-docs-en) to install MeCab system.

### Mecab Neologd dictionary

Mecab-neologd dictionary is a dictionary-extension based on ipadic-dictionary, which is basic dictionary of Mecab.

With, Mecab-neologd dictionary, you're able to parse new-coming words make one token.

Here, new-coming words is such like, movie actor name or company name.....

See [here](https://github.com/neologd/mecab-ipadic-neologd) and install mecab-neologd dictionary.

### Juman

```
wget -O juman7.0.1.tar.bz2 "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2&name=juman-7.01.tar.bz2"
bzip2 -dc juman7.0.1.tar.bz2  | tar xvf -
cd juman-7.01
./configure
make   
[sudo] make install
```    
    

## Juman++

* GCC version must be >= 5

```
wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.02.tar.xz
tar xJvf jumanpp-1.02.tar.xz
cd jumanpp-1.02/
./configure
make
[sudo] make install
```
    
## Kytea

Install Kytea system

```
wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz
tar -xvf kytea-0.4.7.tar
cd kytea-0.4.7
./configure
make
make install
```    


Kytea has [python wrapper](https://github.com/chezou/Mykytea-python) thanks to michiaki ariga.
Install Kytea-python wrapper

```
pip install kytea
```
    

## install

```
[sudo] python setup.py install
```

### Note

During install, you see warning message when it fails to install `pyknp` or `kytea`.

if you see these messages, try to re-install these packages manually.

# Usage

Tokenization Example(For python3.x. To see exmaple code for Python2.x, plaese see [here](https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers/blob/master/examples/examples.py))

```
import JapaneseTokenizer
input_sentence = '10日放送の「中居正広のミになる図書館」（テレビ朝日系）で、SMAPの中居正広が、篠原信一の過去の勘違いを明かす一幕があった。'
# ipadic is well-maintained dictionary #
mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')
print(mecab_wrapper.tokenize(input_sentence).convert_list_object())

# neologd is automatically-generated dictionary from huge web-corpus #
mecab_neologd_wrapper = JapaneseTokenizer.MecabWrapper(dictType='neologd')
print(mecab_neologd_wrapper.tokenize(input_sentence).convert_list_object())
```


## Filtering example

```
import JapaneseTokenizer
# with word filtering by stopword & part-of-speech condition #
print(mecab_wrapper.tokenize(input_sentence).filter(stopwords=['テレビ朝日'], pos_condition=[('名詞', '固有名詞')]).convert_list_object())
```


## Part-of-speech structure

Mecab, Juman, Kytea have different system of Part-of-Speech(POS).

You can check tables of Part-of-Speech(POS) [here](http://www.unixuser.org/~euske/doc/postag/)


# Similar Package


## natto-py

natto-py is sophisticated package for tokenization. It supports following features

* easy interface for tokenization
* importing additional dictionary
* partial parsing mode

# LICENSE

MIT license

# For developers

You could build an environment which has dependencies to test this package.

Simply, you build docker image and run docker container.

## Dev environment

Develop environment is defined with `test/docker-compose-dev.yml`.

With the docker-compose.yml file, you could call python2.7 or python3.7

If you're using Pycharm Professional edition, you could set docker-compose.yml as remote interpreter.

To call python2.7, set `/opt/conda/envs/p27/bin/python2.7`

To call python3.7, set `/opt/conda/envs/p37/bin/python3.7`

## Test environment

These commands checks from procedures of package install until test of package.

```bash
$ docker-compose build
$ docker-compose up
```

