import requests, os, configparser as cp, tkinter
from packaging.version import Version
from packaging import version
from tkinter import messagebox

def show_message(title: str, message: str) -> None:
    root = tkinter.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(title, message, parent=root)
    root.destroy()

def get_version() -> str:
    config = cp.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    return config['Settings']['version']

def get_versions() -> list:
    response = requests.get(f'https://www.richardo.net/files/bukkits')
    result = response.json()
    for i in range(len(result)):
        result[i] = result[i].split("_")[2].replace(".exe", "")
    return result

def get_latest_version() -> str:
    v = get_versions()
    v.sort(key=Version, reverse=True)
    return v[0]

def check_update(now_version: str) -> bool:
    if version.parse(now_version) < version.parse(get_latest_version()):
        return True
    return False

def download(url: str, dir: str, file_name: str) -> None:
    with open(f'{dir}/{file_name}', 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def update(now_version: str) -> None:
    if check_update(now_version):
        download(f'https://www.richardo.net/files/bukkits/dist/버킷_생성기_{get_latest_version()}.exe', '.', f"update.exe")
        os.remove(f"버킷_생성기_{get_version()}.exe")
        os.rename("update.exe", f"버킷_생성기_{get_latest_version()}.exe")
        show_message("업데이트 완료", "업데이트가 완료되었습니다. 프로그램을 재시작합니다.")
        os.system(f"start 버킷_생성기_{get_latest_version()}.exe")

if __name__ == "__main__":    
    update(get_version())

