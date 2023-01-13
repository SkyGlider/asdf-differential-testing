FROM paddlepaddle/paddle:1.6.2-gpu-cuda10.0-cudnn7

COPY ./asr_models/DeepSpeech/setup.sh /DeepSpeech
COPY ./asr_models/DeepSpeech/decoders/swig/setup.sh /DeepSpeech/decoders/swig
RUN apt-get update && apt-get install git -y
WORKDIR /DeepSpeech

RUN pip install paddlepaddle-gpu==1.6.2.post107 && \
    pip install soundfile && \
    pip install llvmlite===0.31.0 && \
    pip install python_speech_features \
    pip install flask

RUN wget -qO - http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz | tar xvz
WORKDIR /DeepSpeech/swig-3.0.12
RUN apt-get install automake -y && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install
WORKDIR /DeepSpeech/decoders/swig
RUN wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.3.tar.gz --no-check-certificate && \
    sh setup.sh

WORKDIR /DeepSpeech
RUN sh setup.sh && \
    apt-get install libsndfile1-dev -y

CMD CUDA_VISIBLE_DEVICES=0 python deepspeech2_api.py --mean_std_path='models/librispeech/mean_std.npz' --vocab_path='models/librispeech/vocab.txt' --model_path='models/librispeech' --lang_model_path='models/lm/common_crawl_00.prune01111.trie.klm'