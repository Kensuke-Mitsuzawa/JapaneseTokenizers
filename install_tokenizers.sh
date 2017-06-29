#!/bin/bash
os_type=`uname`
echo "os-type is "$os_type
if [ `uname` = "Darwin" ]; then
    #mac用のコード
    juman_utils_bin="/usr/local/opt/juman/libexec/juman/"
    if [ -e ${juman_utils_bin} ]; then
        :
    else
        juman_utils_bin="/usr/local/libexec/juman/"
    fi
elif [ `uname` = "Linux" ]; then
    #Linux用のコード
    juman_utils_bin="/usr/local/libexec/juman/"
else
    echo "Your platform ($(uname -a)) is not supported."
    exit 1
fi

WORK_DIR=`pwd`
echo 'これはテスト' | mecab
is_mecab_install=$?

if [ $is_mecab_install -eq 127 ]; then
    ## mecab
    wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
    tar zxvf mecab-0.996.tar.gz
    cd mecab-0.996 && ./configure && make && make install
    cd $WORK_DIR

    ### mecabインストール後にldconfigを実行
    ldconfig

    ## mecab ipadic
    wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
    tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz
    cd mecab-ipadic-2.7.0-20070801 &&./configure --with-charset=utf8 && make && make install
    # 動作テスト
    echo 'インストール後のテスト' | mecab
else
    :
fi

echo 'これはテスト' | juman
is_juman_install=$?

if [ $is_juman_install -eq 127 ]; then
    ## juman
    wget -O juman7.0.1.tar.bz2 "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2&name=juman-7.01.tar.bz2"
    bzip2 -dc juman7.0.1.tar.bz2  | tar xvf -
    cd juman-7.01 && ./configure && make && make install

    # インストール後のldconfig
    ldconfig
    # 動作テスト
    echo 'インストール後のテスト' | juman
else
    :
fi

echo 'これはテスト' | jumanpp
is_jumanpp_install=$?

if [ $is_jumanpp_install -eq 127 ]; then
    # jumanpp
    wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.01.tar.xz
    tar xJvf jumanpp-1.01.tar.xz
    cd jumanpp-1.01/ && ./configure && make && make install
    # todo jumanppのサーバー起動スクリプト実施

    # インストール後のldconfig
    ldconfig
    # 動作テスト
    echo 'インストール後のテスト' | jumanpp
else
    :
fi


echo 'これはテスト' | kytea
is_kytea_install=$?

if [ $is_kytea_install -eq 127 ]; then
    # kytea
    wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz -O kytea-0.4.7.tar.gz
    tar -xvf kytea-0.4.7.tar.gz
    cd kytea-0.4.7 && ./configure && make && make install
    # インストール後のldconfig
    ldconfig
    # 動作テスト
    echo 'インストール後のテスト' | kytea
else
    :
fi


if [ -f ./juman7.0.1.tar.bz2 ]; then
    # juman
	rm juman7.0.1.tar.bz2
else
    :
fi

if [ -f ./mecab-*.tar.gz ]; then
    # juman
	rm mecab-*.tar.gz
else
    :
fi

if [ -f ./mecab-ipadic-*.tar.gz ]; then
	# mecab-ipadic
	rm mecab-ipadic-*.tar.gz
else
    :
fi


if [ -f ./jumanpp-1.01.tar.xz ]; then
	# jumanpp
	rm jumanpp-1.01.tar.xz
else
    :
fi


if [ -f ./kytea-0.4.7.tar ]; then
	# kytea
	rm kytea-0.4.7.tar
else
    :
fi


if [ -d ./juman-7* ]; then
	# kytea
	rm -rf juman-7*
else
    :
fi

if [ -d ./mecab-0* ]; then
	# kytea
	rm -rf mecab-0*
else
    :
fi

if [ -d ./mecab-ipadic-* ]; then
	rm -rf mecab-ipadic-*
else
    :
fi

if [ -d ./jumanpp-1.01 ]; then
	rm -rf jumanpp-1.01
else
    :
fi

if [ -d ./kytea-0.4.7 ]; then
	rm -rf kytea-0.4.7
else
    :
fi