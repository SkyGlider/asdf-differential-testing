# ASDF Differential Testing Tool

Automatic testing tools for Automatic Speech Recognition (ASR) systems are used to uncover failed test cases using  ASDF is a differential testing framework for ASR systems. ASDF leverages upon [CrossASR++](https://github.com/soarsmu/CrossASRplus), an existing ASR testing tool that automates the audio test case generation process, and further improves it by incorporating differential testing methods. CrossASR++ selects texts from an input text corpus, converts them into audio using a Text-to-Speech (TTS) service, and uses the audio to test the ASR systems. However, the quality of these tests greatly depend on the quality of the text corpus provided, and may not uncover underlying weaknesses of the ASRs due to the text's limited variation and vocabulary. 

Here, ASDF builds upon CrossASR++ by incoprporating differential testing for ASR systems by applying text transformation methods to the original text inputs that failed in the CrossASR++ ASR testing process, effectively creating new high-quality test cases for ASR systems. We also improved the tool's usability by including a CLI for easier use.

Please check out our (Tool Demonstration video)[] and (PDF preprint)[].

## Initial Setup

### WSL
1. Set up WSL to use Linux in Windows. [Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
2. To access Window files in WSL: WSL mounts your machine's fixed drives under the /mnt/<drive> folder in your Linux distros. For example, your C: drive is mounted under /mnt/c/
3. It is recommended to store your local repo under your Linux distro home directory instead of /mnt/<drive>/... because differing file naming systems will cause issues (eg. filename is not case sensitive in Windows file system)
4. To connect to the Internet, change the `nameserver` in `etc/resolv.conf` to 8.8.8.8. [Stackoverflow](https://stackoverflow.com/questions/62314789/no-internet-connection-on-wsl-ubuntu-windows-subsystem-for-linux)
5. `etc/resolv.conf` will reset everytime you restart WSL. To solve this issue, look at this [post](https://askubuntu.com/questions/1347712/make-etc-resolv-conf-changes-permanent-in-wsl-2)

### Docker Desktop
1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. If you are using WSL, set up Docker Desktop for Windows with WSL 2. [Guide](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

## Usage
Go to the `example` directory using 
`cd asdf-differential-testing/CrossASRplus/examples`

Execute the batch file
