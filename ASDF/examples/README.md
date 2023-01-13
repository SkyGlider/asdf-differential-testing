# Usage of ASDDF

1. [Enable WSL](##1-enable-wsl)
2. [Install Python](##2-install-python)
3. [Install Docker and Pull Wav2letter Container](##3-install-docker)
4. [Laucnh ASDF](##4-launch-asdf)

## 1. Enable Wsl

### 1.1. Follow this link to enable Windows Subsystem for Linux

Please follow [this link for the turtorial](https://learn.microsoft.com/en-us/windows/wsl/install)

### 1.2. Install Ubuntu Image from Microsoft Store

https://apps.microsoft.com/store/detail/ubuntu-on-windows/9NBLGGH4MSV6?hl=en-us&gl=us


### 1.3. Launch WSL

```bash
wsl -d Ubuntu
```

## 2. Install Python 3.8 

Note: Newer versions of python does not work!

### 2.1 Add deadsnakes repository

```bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
```

### 2.2. Install Python 3.8 and Python 3.8 venv

```bash
sudo apt install python 3.8 python3.8-venv
```

## 3. Install Docker and pull ASR Images

### 3.1. Install Docker Dekstop

Please follow [this link to install docker](https://www.docker.com/products/docker-desktop/).


### 3.2. Deepspeech2

[DeepSpeech2](https://github.com/PaddlePaddle/DeepSpeech) is an open-source implementation of end-to-end Automatic Speech Recognition (ASR) engine, based on [Baidu's Deep Speech 2 paper](http://proceedings.mlr.press/v48/amodei16.pdf), with [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) platform.

#### Setup a docker container for Deepspeech2

[Original Source](https://github.com/PaddlePaddle/DeepSpeech#running-in-docker-container)

```bash
cd asr_models/
git clone https://github.com/PaddlePaddle/DeepSpeech.git
cd DeepSpeech
git checkout tags/v1.1
cp ../../asr/deepspeech2_api.py .
cd models/librispeech/
sh download_model.sh
cd ../../../../
cd asr_models/DeepSpeech/models/lm
sh download_lm_en.sh
cd ../../../../
docker pull paddlepaddle/paddle:1.6.2-gpu-cuda10.0-cudnn7

# run this command from examples folder
# please remove --gpus '"device=1"' if you only have one gpu
docker run --name deepspeech2 --rm --gpus '"device=1"' -it -v $(pwd)/asr_models/DeepSpeech:/DeepSpeech -v $(pwd)/output/:/DeepSpeech/output/  paddlepaddle/paddle:1.6.2-gpu-cuda10.0-cudnn7 /bin/bash

apt-get update
apt-get install git -y
cd DeepSpeech
sh setup.sh
apt-get install libsndfile1-dev -y
``` 

**in case you found error when running the `setup.sh`**

Error solution for `ImportError: No module named swig_decoders`
```bash
pip install paddlepaddle-gpu==1.6.2.post107
cd DeepSpeech
pip install soundfile
pip install llvmlite===0.31.0
pip install resampy
pip install python_speech_features

wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz
tar xvzf swig-3.0.12.tar.gz
cd swig-3.0.12
apt-get install automake -y 
./autogen.sh
./configure
make
make install

cd ../decoders/swig/
sh setup.sh
cd ../../
```

#### Run Deepspeech2 as an API (inside docker container)
```bash
pip install flask 

# run inside /DeepSpeech folder in the container
CUDA_VISIBLE_DEVICES=0 python deepspeech2_api.py \
    --mean_std_path='models/librispeech/mean_std.npz' \
    --vocab_path='models/librispeech/vocab.txt' \
    --model_path='models/librispeech' \
    --lang_model_path='models/lm/common_crawl_00.prune01111.trie.klm'
```
Then detach from the docker using ctrl+p & ctrl+q after you see `Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

#### Run Client from the Terminal (outside docker container)

```bash
# run from examples folder in the host machine (outside docker)
docker exec -it deepspeech2 curl http://localhost:5000/transcribe?fpath=output/audio/google/hello.wav
```

### 3.3. Wav2letter++

[wav2letter++](https://github.com/facebookresearch/wav2letter) is a highly efficient end-to-end automatic speech recognition (ASR) toolkit written entirely in C++ by Facebook Research, leveraging ArrayFire and flashlight.

Please find the lastest image of [wav2letter's docker](https://hub.docker.com/r/wav2letter/wav2letter/tags).

```bash
cd asr_models/
mkdir wav2letter
cd wav2letter

for f in acoustic_model.bin tds_streaming.arch decoder_options.json feature_extractor.bin language_model.bin lexicon.txt tokens.txt ; do wget http://dl.fbaipublicfiles.com/wav2letter/inference/examples/model/${f} ; done

ls -sh
cd ../../
```

#### Run docker inference API
```bash
# run from examples folder
docker run --name wav2letter -it --rm -v $(pwd)/output/:/root/host/output/ -v $(pwd)/asr_models/:/root/host/models/ --ipc=host -a stdin -a stdout -a stderr wav2letter/wav2letter:inference-latest
```
Then detach from the docker using ctrl+p & ctrl+q 

#### Run Client from the Terminal

```bash
docker exec -it wav2letter sh -c "cat /root/host/output/audio/google/hello.wav | /root/wav2letter/build/inference/inference/examples/simple_streaming_asr_example --input_files_base_path /root/host/models/wav2letter/"
```

Detail of [wav2letter++ installation](https://github.com/facebookresearch/wav2letter/wiki#Installation) and [wav2letter++ inference](https://github.com/facebookresearch/wav2letter/wiki/Inference-Run-Examples)

## 4. Running ASDF

Launch the batch file start.bat on a windows machine, it will automatically install all dependencies of ASDF and launcht eh ASDF tool.


## 5. Running ASDF (skipping dependency installation)

This method will skip the dependency installation phase and immedaitely launch the ASDF tool.  

```bash
python app.py
``` 

## 6. References

ASDF is built on [CrossASR++](https://github.com/soarsmu/CrossASRplus)

