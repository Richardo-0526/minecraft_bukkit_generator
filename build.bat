@echo off
set /p V=���� �Է� (v ����) :
cd "C:\xampp\htdocs\files\bukkits"
pyinstaller -w -F "C:\Users\Administrator\Desktop\FTP\23_��Ŷ����\bukkit_maker.py" -n ��Ŷ_������_v%V% -i "C:\Users\Administrator\Desktop\FTP\23_��Ŷ����\icon.ico" --add-data ""C:\Users\Administrator\Desktop\FTP\23_��Ŷ����\resources";resources"
TIMEOUT 5 /NOBREAK
exit