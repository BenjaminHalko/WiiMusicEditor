@echo off

cd "%~dp0"
cd..
cd..
cd..

robocopy "%CD%%1" "%CD%" /E /MIR /XF settings.ini /XD .git

python WiiMusicEditor.py