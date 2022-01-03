@echo off

call %~dp0pythonProject2\venv\Scripts\activate

cd %~dp0pythonProject2
set TOKEN=2119047086:AAG2tUZmRULNasX8Rkb1tTUb4uEDwkQ640k
python main.py

pause