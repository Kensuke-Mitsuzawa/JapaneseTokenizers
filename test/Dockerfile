FROM frolvlad/alpine-glibc:alpine-3.6
MAINTAINER kensuke-mi <kensuke.mit@gmail.com>

# Mecab install
ENV MECAB_VERSION 0.996
ENV IPADIC_VERSION 2.7.0-20070801
ENV mecab_url https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE
ENV ipadic_url https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM
ENV build_deps 'curl git bash file sudo openssh gcc make build-base'
ENV dependencies 'openssl'

ENV PATH=/opt/conda/bin:$PATH \
    LANG=C.UTF-8 \
    MINICONDA=Miniconda3-latest-Linux-x86_64.sh
# apk update
RUN apk update

# mecab
RUN apk add --update --no-cache ${build_deps} \
  # Install dependencies
  && apk add --update --no-cache ${dependencies} \
  # Install MeCab
  && curl -SL -o mecab-${MECAB_VERSION}.tar.gz ${mecab_url} \
  && tar zxf mecab-${MECAB_VERSION}.tar.gz \
  && cd mecab-${MECAB_VERSION} \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  # Install IPA dic
  && curl -SL -o mecab-ipadic-${IPADIC_VERSION}.tar.gz ${ipadic_url} \
  && tar zxf mecab-ipadic-${IPADIC_VERSION}.tar.gz \
  && cd mecab-ipadic-${IPADIC_VERSION} \
  && ./configure --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  # Install Neologd
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
  && mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y \
  && rm -rf \
    mecab-${MECAB_VERSION}* \
    mecab-${IPADIC_VERSION}* \
    mecab-ipadic-neologd

# general
RUN apk --no-cache add vim \
wget \
lsof \
curl \
bash \
swig \
gcc \
build-base \
make \
python-dev \
py-pip \
jpeg-dev \
zlib-dev \
git \
linux-headers
ENV LIBRARY_PATH=/lib:/usr/lib

ENV PLANTUML_VERSION 1.2017.18
ENV PLANTUML_DOWNLOAD_URL https://sourceforge.net/projects/plantuml/files/plantuml.$PLANTUML_VERSION.jar/download
ENV PANDOC_VERSION 1.19.2.4
ENV PANDOC_DOWNLOAD_URL https://hackage.haskell.org/package/pandoc-$PANDOC_VERSION/pandoc-$PANDOC_VERSION.tar.gz
ENV PANDOC_ROOT /usr/local/pandoc

ENV PATH $PATH:$PANDOC_ROOT/bin

# Create Pandoc build space
RUN mkdir -p /pandoc-build
WORKDIR /pandoc-build

# Install/Build Packages
RUN apk upgrade --update && \
    apk add --no-cache --virtual .build-deps $BUILD_DEPS && \
    apk add --no-cache --virtual .persistent-deps $PERSISTENT_DEPS && \
    curl -fsSL "$PLANTUML_DOWNLOAD_URL" -o /usr/local/plantuml.jar && \
    apk add --no-cache --virtual .edge-deps $EDGE_DEPS -X http://dl-cdn.alpinelinux.org/alpine/edge/community && \
    curl -fsSL "$PANDOC_DOWNLOAD_URL" | tar -xzf - && \
        ( cd pandoc-$PANDOC_VERSION && cabal update && cabal install --only-dependencies && \
        cabal configure --prefix=$PANDOC_ROOT && \
        cabal build && \
        cabal copy && \
        cd .. ) && \
    rm -Rf pandoc-$PANDOC_VERSION/ && \
    rm -Rf /root/.cabal/ /root/.ghc/ && \
    rmdir /pandoc-build && \
    set -x; \
    addgroup -g 82 -S www-data; \
    adduser -u 82 -D -S -G www-data www-data && \
    mkdir -p /var/docs && \
    apk del .build-deps .edge-deps

# Juman
RUN wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2 \
    && tar xvf juman-7.01.tar.bz2 \
    && cd juman-7.01 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf juman-7.01 \
    && rm juman-7.01.tar.bz2

# Juman++
RUN apk add --update --no-cache --virtual=build-deps \
    boost-dev g++ make \
    && wget -q http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.02.tar.xz \
    && tar Jxfv jumanpp-1.02.tar.xz \
    && cd jumanpp-1.02/ \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm jumanpp-1.02.tar.xz \
    && rm -rf /var/cache/* \
    && apk del build-deps \
    && apk add --update --no-cache boost

# kytea
RUN wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz \
    && tar -xvf kytea-0.4.7.tar.gz \
    && cd kytea-0.4.7 \
    && ./configure \
    && make \
    && make install

# Python
RUN apk add --no-cache bash wget && \
    wget -q --no-check-certificate https://repo.continuum.io/miniconda/$MINICONDA && \
    bash $MINICONDA -b -p /opt/conda && \
    ln -s /opt/conda/bin/* /usr/local/bin/ && \
    rm -rf /root/.[acpw]* $MINICONDA /opt/conda/pkgs/*

RUN conda config --add channels conda-forge --system
RUN conda create -y -n p27 python=2.7
RUN conda create -y -n p36 python=3.6
RUN conda create -y -n p37 python=3.7

#RUN source activate p27
#RUN source deactivate

CMD ["/bin/bash"]