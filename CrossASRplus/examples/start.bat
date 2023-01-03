@echo off

TITLE ASR Differential Testing Tool
ECHO Thanks for using the ASR differential testing tool.
ECHO Checking for dependencies...

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