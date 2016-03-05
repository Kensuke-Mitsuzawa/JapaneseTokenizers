# What's this?

This is simple wrapper for Japanese Tokenizers(A.K.A Morphology Splitter)

This repository aims to call Tokenizer and split into tokens in one line.

If you find any bugs, please report them to github issues. Or any pull requests are welcomed!

# Requirements

* Python 2.7
* Python 3.5


# Features

* You can get set of tokens from input sentence
* You can filter some tokens with your Part-of-Speech condition or stopwords
* You can add extension dictionary like mecab-neologd dictionary
* You can define your original dictionary. And this dictionary forces mecab to make it one token
 
# Setting up


## MeCab system

See [here](https://github.com/jordwest/mecab-docs-en) to install MeCab system.

## Mecab Neologd dictionary

Mecab-neologd dictionary is a dictionary-extension based on ipadic-dictionary, which is basic dictionary of Mecab.

With, Mecab-neologd dictionary, you're able to new-coming words make one token.

Here, new-coming words is suche like, movie actor name or company name.....

See [here](https://github.com/neologd/mecab-ipadic-neologd) and install mecab-neologd dictionary.


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
