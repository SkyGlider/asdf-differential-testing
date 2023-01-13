#!/bin/bash

if [ ! -d ~/./env ]; then python3.8 -m venv --system-site-packages ~/./env; fi

source ~/./env/bin/activate

pip install -r requirements.txt
python -c "import nltk;nltk.download('brown');nltk.download('names');nltk.download('stopwords');nltk.download('omw-1.4');nltk.download('words')"

if [ ! -d "output/" ]; then mkdir output/; fi
if [ ! -d "output/audio/" ]; then mkdir output/audio/; fi
if [ ! -d "asr_models/" ]; then mkdir asr_models; fi

cd asr_models
if [ ! -d "deepspeech/" ]; then mkdir deepspeech; cd deepspeech; curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm;  curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer; cd ../; fi
if [ ! -d "wav2letter/" ]; then mkdir wav2letter; cd wav2letter; for f in acoustic_model.bin tds_streaming.arch decoder_options.json feature_extractor.bin language_model.bin lexicon.txt tokens.txt ; do wget http://dl.fbaipublicfiles.com/wav2letter/inference/examples/model/${f} ; done; ls -sh; cd ../; fi
docker run --name wav2letter -it --rm -v $(pwd)/output/:/root/host/output/ -v $(pwd)/asr_models/:/root/host/models/ --ipc=host -a stdin -a stdout -a stderr wav2letter/wav2letter:inference-latest
cd ../

python -m spacy download en_core_web_sm

cd ../
pip install .
cd examples

python3 app.py