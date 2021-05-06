@echo off

cd "%~dp0"
cd..
cd..

del /f /s /q tmp 1>nul
rmdir /s /q tmp 1>nul