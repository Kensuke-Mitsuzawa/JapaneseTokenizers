install:
	bash install_tokenizers.sh

install_neologd:
	## mecab-neologdのインストールを実行
	wget --no-check-certificate https://github.com/neologd/mecab-ipadic-neologd/tarball/master -O mecab-ipadic-neologd.tar
	tar -xvf mecab-ipadic-neologd.tar
	mv neologd-mecab-ipadic-neologd-* neologd-mecab-ipadic-neologd && cd neologd-mecab-ipadic-neologd && ( echo yes | ./bin/install-mecab-ipadic-neologd )