@echo off
cd /d "%~dp0"
python MAA_log_send.py
python check_MAA_emulator.py