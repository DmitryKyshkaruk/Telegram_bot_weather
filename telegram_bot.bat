@echo off

call %~dp0venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN= bot token here

python bot_telegram.py

pause