#!/bin/bash

if [ ! -d ~/./env ]; then python3.8 -m venv --system-site-packages ~/./env; fi

source ~/./env/bin/activate

if [ ! -d "output/" ]; then mkdir output/; fi
if [ ! -d "output/audio/" ]; then mkdir output/audio/; fi

pip install gTTS
pip install rvtts

if [ ! -d "asr_models/" ]; then mkdir asr_models; fi

pip install deepspeech===0.9.3
cd asr_models

if [ ! -d "deepspeech/" ]; then mkdir deepspeech; cd asr_models/deepspeech; curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm;  curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer; fi

cd asr_models
if [ ! -d "wav2letter/" ]; then mkdir wav2letter; cd asr_models/wav2letter; for f in acoustic_model.bin tds_streaming.arch decoder_options.json feature_extractor.bin language_model.bin lexicon.txt tokens.txt ; do wget http://dl.fbaipublicfiles.com/wav2letter/inference/examples/model/${f} ; done; ls -sh; fi
docker run --name wav2letter -it --rm -v $(pwd)/output/:/root/host/output/ -v $(pwd)/asr_models/:/root/host/models/ --ipc=host -a stdin -a stdout -a stderr wav2letter/wav2letter:inference-latest

pip install wit
export WIT_ACCESS_TOKEN=A

bash install_requirement.sh 

pip install torch
pip install transformers

pip install wordhoard
pip install pyinflect
pip install inflect
pip install spacy
python -m spacy download en_core_web_sm

cd ../
pip install .
cd CrossASRplus
python3 app.py