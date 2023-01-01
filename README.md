# asr-fuzzing-testing

## Initial Setup

### WSL
- Set up WSL to use Linux from Window. [Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
- It's recommended to store your local repo under linux home directory instead of /mnt/<drive>/... because the file naming will cause issue (eg. filename is not case sensitive in Window file system)
- To access Window files in WSL: WSL mounts your machine's fixed drives under the /mnt/<drive> folder in your Linux distros. For example, your C: drive is mounted under /mnt/c/
- To connect to internet, change the `nameserver` in `etc/resolv.conf` to 8.8.8.8
[Stackoverflow](https://stackoverflow.com/questions/62314789/no-internet-connection-on-wsl-ubuntu-windows-subsystem-for-linux)
- `etc/resolv.conf` will reset everytime you restart WSL. To solve this issue, look at this [post](https://askubuntu.com/questions/1347712/make-etc-resolv-conf-changes-permanent-in-wsl-2)

### Jupyter notebook in WSL
1. How to create venv with python3.8 (python3.10 doesn't work) [Stackoverflow](https://stackoverflow.com/questions/70422866/how-to-create-a-venv-with-a-different-python-version)
2. Activate venv using `source env/bin/activate`
3. Open Jupyter notebook using `jupyter notebook`
4. Run this only once after you have set up venv `bash install_requirement.sh`

### Packages to install
1. ffmpeg: `sudo apt install ffmpeg`
2. festival: `sudo apt install festival`
3. espeak: `sudo apt install espeak`

### Docker
1. Download Docker Desktop
2. If you are using WSL. You need to do this. [Guide](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

### Commands to run test_asr.py
1. Go to example directory: `cd asr-fuzzing-testing/CrossASRplus/examples`
2. Activate your venv `source ../env/bin/activate` (might be different path for you)
3. Start docker container: `docker run --name wav2letter -it --rm -v "$(pwd)/data/:/root/host/data/" -v "$(pwd)/output/:/root/host/output/" -v "$(pwd)/asr_models/:/root/host/models/" --ipc=host -a stdin -a stdout -a stderr wav2letter/wav2letter:inference-latest`
4. Set your environment (or you can make it persistent): `export WIT_ACCESS_TOKEN=<your_token>`
5. Test if everything works: `python cross_reference.py config_corpus.json`
6. Run test_asr.py: `python test_asr.py config_corpus.json`
