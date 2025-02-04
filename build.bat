@echo off
set /p V=버전 입력 (v 생략) :
cd "C:\xampp\htdocs\files\bukkits"
pyinstaller -w -F "C:\Users\Administrator\Desktop\FTP\23_버킷제작\bukkit_maker.py" -n 버킷_생성기_v%V% -i "C:\Users\Administrator\Desktop\FTP\23_버킷제작\icon.ico" --add-data ""C:\Users\Administrator\Desktop\FTP\23_버킷제작\resources";resources"
TIMEOUT 5 /NOBREAK
exit