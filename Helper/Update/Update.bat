@echo off

cd "%~dp0"
cd..
cd..
cd..

robocopy "%CD%%1" "%CD%" /MIR /XF settings.ini /XD "%CD%%1" .git

rm WiiMusicEditor.zip
python WiiMusicEditor.py