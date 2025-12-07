@echo off
echo Starting MarineCode components...
start "MarineCode Main" python start_marinecode.py
start "MarineCode Agent" /D "MarineCode_4.0\MarineCode-Main" python agent.py console
echo Both components started in separate windows.
pause