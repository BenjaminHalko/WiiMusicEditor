@echo off

cd "%~dp0"
cd..
cd..
cd..

robocopy "%CD%\WiiMusicEditorNew" "%CD%" /MIR /XF settings.ini /XD .git WiiMusicEditorNew > nul

WiiMusicEditor.bat