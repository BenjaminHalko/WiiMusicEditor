@echo off

cd "%~dp0"
cd..
cd..
cd..

robocopy "%CD%\WiiMusicEditor" "%CD%" /MIR /XF settings.ini /XD .git WiiMusicEditor > nul

python "WiiMusicEditor.py"