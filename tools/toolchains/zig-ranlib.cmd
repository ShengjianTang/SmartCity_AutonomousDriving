@echo off
setlocal
"%~dp0..\..\.venv\Scripts\python-zig.exe" ranlib %*
exit /b %ERRORLEVEL%
