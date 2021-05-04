@echo off

cd "%~dp0"
cd..
cd..
cd..

echo robocopy "%CD%%1" "%CD%" /MIR /XF settings.ini /XD .git "%CD%%1"

timeout 30