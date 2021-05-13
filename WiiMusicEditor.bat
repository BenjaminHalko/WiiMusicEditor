@echo off

cd %~dp0"
python "WiiMusicEditor.py" %1
if not exist WiiMusicEditorNew pause