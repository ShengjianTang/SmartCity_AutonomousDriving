@echo off
setlocal
"%~dp0..\..\.venv\Scripts\python-zig.exe" ar %*
exit /b %ERRORLEVEL%
