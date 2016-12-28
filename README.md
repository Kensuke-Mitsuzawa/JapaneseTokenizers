# What's this?

This is simple wrapper for Japanese Tokenizers(A.K.A Morphology Splitter)

This project aims to call Tokenizer and split into tokens as easy as possible.

And this project supports various Tokenization tools. You can compare results among them.

This project is available also in [Github](https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers).  

If you find any bugs, please report them to github issues. Or any pull requests are welcomed!

# Requirements

* Python 2.7
* Python 3.5


# Features

* You can get set of tokens from input sentence
* You can filter some tokens with your Part-of-Speech condition or stopwords
* You can add extension dictionary like mecab-neologd dictionary
* You can define your original dictionary. And this dictionary forces mecab to make it one token

## Supported Tokenization tool

### Mecab

[Mecab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html?sess=3f6a4f9896295ef2480fa2482de521f6) is open source tokenizer system for various language(if you have dictionary for it)

See [english documentation](https://github.com/jordwest/mecab-docs-en) for detail

### Juman

[Juman](http://nlp.ist.i.kyoto-u.ac.jp/EN/index.php?JUMAN) is tokenizer tool developped by Kurohashi laboratory, Kyoto University, Japan.

Juman is strong for ambigious writing style in Japanese, and is strong for new-comming words thanks to Web based huge dictionary.
 
And, Juman tells you semantic meaning of words.

### Juman++

[Juman++](http://nlp.ist.i.kyoto-u.ac.jp/EN/index.php?JUMAN++) is tokenizer  developped by Kurohashi laboratory, Kyoto University, Japan.

Juman++ is succeeding system of Juman. It adopts RNN model for tokenization.

Juman++ is strong for ambigious writing style in Japanese, and is strong for new-comming words thanks to Web based huge dictionary.
 
And, Juman tells you semantic meaning of words.


### Kytea

[Kytea](http://www.phontron.com/kytea/) is tokenizer tool developped by Graham Neubig.

Kytea has a different algorithm from one of Mecab or Juman. 

 
# Setting up


## MeCab

See [here](https://github.com/jordwest/mecab-docs-en) to install MeCab system.

## Mecab Neologd dictionary

Mecab-neologd dictionary is a dictionary-extension based on ipadic-dictionary, which is basic dictionary of Mecab.

With, Mecab-neologd dictionary, you're able to parse new-coming words make one token.

Here, new-coming words is such like, movie actor name or company name.....

See [here](https://github.com/neologd/mecab-ipadic-neologd) and install mecab-neologd dictionary.

## Juman

    wget -O juman7.0.1.tar.bz2 "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2&name=juman-7.01.tar.bz2"
    bzip2 -dc juman7.0.1.tar.bz2  | tar xvf -
    cd juman-7.01
    ./configure
    make   
    [sudo] make install
    
## Juman++

* GCC version must be >= 5

```
wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.01.tar.xz
tar xJvf jumanpp-1.01.tar.xz
cd jumanpp-1.01/
./configure
make
[sudo] make install
```
    
## Kytea

Install Kytea system

    wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz
    tar -xvf kytea-0.4.7.tar
    cd kytea-0.4.7
    ./configure
    make
    make install


Kytea has [python wrapper](https://github.com/chezou/Mykytea-python) thanks to michiaki ariga.
Install Kytea-python wrapper

    pip install kytea
    
# Part-of-speech structure

Mecab, Juman uses different system of Part-of-Speech(POS).

Keep in your mind when you use it.

You can check tables of Part-of-Speech(POS) [here](http://www.unixuser.org/~euske/doc/postag/)

## install

```
[sudo] python setup.py install
```

# Usage


Tokenization Example(For python2x. To see exmaple code for Python3.x, plaese see [here](https://github.com/Kensuke-Mitsuzawa/JapaneseTokenizers/blob/master/examples/examples.py))

    # input is `unicode` type(in python2x)
    sentence = u'テヘラン（ペルシア語: تهران  ; Tehrān Tehran.ogg 発音[ヘルプ/ファイル]/teɦˈrɔːn/、英語:Tehran）は、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'

    # make MecabWrapper object
    # path where `mecab-config` command exists. You can check it with `which mecab-config`
    # default value is '/usr/local/bin'
    path_mecab_config='/usr/local/bin'

    # you can choose from "neologd", "all", "ipaddic", "user", ""
    # "ipadic" and "" is equivalent
    dictType = ""

    mecab_wrapper = MecabWrapper(dictType=dictType, path_mecab_config=path_mecab_config)

    # tokenize sentence. Returned object is list of tuples
    tokenized_obj = mecab_wrapper.tokenize(sentence=sentence)
    assert isinstance(tokenized_obj, list)

    # Returned object is "TokenizedSenetence" class if you put return_list=False
    tokenized_obj = mecab_wrapper.tokenize(sentence=sentence, return_list=False)


Filtering example

    stopwords = [u'テヘラン']
    assert isinstance(tokenized_obj, TokenizedSenetence)
    # returned object is "FilteredObject" class
    filtered_obj = mecab_wrapper.filter(
        parsed_sentence=tokenized_obj,
        stopwords=stopwords
    )
    assert isinstance(filtered_obj, FilteredObject)

    # pos condition is list of tuples
    # You can set POS condition "ChaSen 品詞体系 (IPA品詞体系)" of this page http://www.unixuser.org/~euske/doc/postag/#chasen
    pos_condition = [(u'名詞', u'固有名詞'), (u'動詞', u'自立')]
    filtered_obj = mecab_wrapper.filter(
        parsed_sentence=tokenized_obj,
        pos_condition=pos_condition
    )


# Similar Package


## natto-py

natto-py is sophisticated package for tokenization. It supports following features

* easy interface for tokenization
* importing additional dictionary
* partial parsing mode


# CHANGES


## 0.6(2016-03-05)

* first release to Pypi

## 0.7(2016-03-06)

* Juman supports(only for python2.x)
* Kytea supports(only for python2.x)

## 0.8(2016-04-03)

* removed a bug when interface calls JUMAN
* fixed the version number of jctconv
 
## 0.9 (2016-04-05)

* Kytea supports also for Python3.x(Thanks to @chezou)

## 1.0 (2016-06-19)

* Juman supports also for Python3.x

## 1.2.5 (2016-12-28)

* It fixed bugs in Juman server mode in python3.x
* It supports Juman++
* It supports `filter` method with chain expression