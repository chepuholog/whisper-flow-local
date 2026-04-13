@echo off
PowerShell -Command "Start-Process python -ArgumentList 'main.py' -WorkingDirectory '%~dp0' -Verb RunAs -WindowStyle Hidden"
