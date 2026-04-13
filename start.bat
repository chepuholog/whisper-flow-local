@echo off
cd /d "%~dp0"
PowerShell -Command "Start-Process pythonw -ArgumentList 'main.py' -WorkingDirectory '%~dp0' -Verb RunAs"
