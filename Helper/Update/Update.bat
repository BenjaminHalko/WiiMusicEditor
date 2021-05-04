@echo off

cd "%~dp0"
cd..
cd..
cd..

robocopy "%CD%\%1" "%CD%" /MIR /XF settings.ini /XD .git %1

python "WiiMusicEditor.py" nothing