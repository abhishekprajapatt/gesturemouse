REM filepath: d:\AbhiSDE\Projects\system-dev\gesturemouse\build_exe.bat
@echo off
echo Installing pyinstaller if needed...
pip install pyinstaller
echo.
echo Building GestureMouse.exe...
pyinstaller --onefile --windowed --name GestureMouse main.py
echo.
echo Done! Check dist folder for GestureMouse.exe
pause