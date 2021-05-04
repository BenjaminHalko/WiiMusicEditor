@echo off

cd %~dp0"
cd..
python "WiiMusicEditor.py" %1

timeout 60