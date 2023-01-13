@echo off

TITLE ASDF - ASR Differential Testing Tool
ECHO Thanks for using ASDF, an ASR differential testing tool.
ECHO Please wait while we check and install dependencies...

WHERE wsl >nul 2>nul
IF %ERRORLEVEL% NEQ 0 ECHO wsl wasn't found please enable and install wsl.

wsl -u root apt update
wsl -u root add-apt-repository ppa:deadsnakes/ppa;
wsl -u root apt install python3.8 python3-pip python3.8-venv;
wsl -u root apt install ffmpeg
wsl -u root apt install festival
wsl -u root apt install espeak
wsl bash start-venv.sh

pause