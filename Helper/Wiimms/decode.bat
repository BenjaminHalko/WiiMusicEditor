@echo off

if exist %1\message.d\ (rmdir /s /q %1\message.d)
wszst.exe extract %1\message.carc
del %1\message.d\wszst-setup.txt
wbmgt.exe decode %1\message.d\new_music_message.bmg
del %1\message.d\new_music_message.bmg