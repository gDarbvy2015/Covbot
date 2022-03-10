FROM ubuntu:latest
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Vienna
RUN apt-get -y install wget
RUN apt-get -y install unzip
RUN apt-get -y install openjdk-17-jre
RUN cd ~
RUN wget https://nlp.stanford.edu/software/stanford-corenlp-latest.zip
RUN unzip stanford-corenlp-latest.zip
RUN cd stanford-corenlp-4.4.0
# RUN java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -preload "tokenize, ssplit, pos, lemma, ner"