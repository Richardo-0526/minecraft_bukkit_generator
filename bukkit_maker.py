import tkinter as tk, tkinter.ttk as ttk, requests, xmltodict, os, shutil as su, re, sv_ttk, darkdetect, pywinstyles, sys, base64, zlib, tempfile, configparser as cp, codecs, chardet, threading
from packaging.version import Version
from packaging import version as vv
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import filedialog, messagebox, font as ft

# ------------- 기본 변수

version = 'v1.7.6'

difficulties = ["평화로움", "쉬움", "보통", "어려움"]
difficulties_en = ["peaceful", "easy", "normal", "hard"]
gamemodes = ["서바이벌", "크리에이티브", "모험", "관전"]
gamemodes_en = ["survival", "creative", "adventure", "spectator"]
leveltypes = ["기본", "평지", "확장된 바이옴", "증폭"]
leveltypes_en = ["default", "flat", "largeBiomes", "amplified"]
plugins = []
mods = []
map_folder = ""

gamemode = 0
difficulty = 1
level_type = 0
pvp = True
spawn_protection = 16
allow_flight = False
max_players = 20
allow_command_block = False
port = 25565
whitelist = False
motd = "A Minecraft Server"
motd_P = "A Minecraft Server"

server_f_status = True
plugins_status = False
mods_status = False

bukkit_list = ["Vanilla", "Paper", "Purpur", "Plazma", "Leaves", "Pufferfish", "Folia", "Forge", "NeoForge", "Fabric", "Mohist", "CatServer", "Arclight", "Velocity", "SpongeVanilla"]

# ------------- 기본 변수

def show_message(title: str, message: str) -> None:
    root = tk.Tk()
    root.wm_attributes('-toolwindow', 'True')
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(title, message, parent=root)
    root.destroy()

def show_error(title: str, message: str) -> None:
    root = tk.Tk()
    root.wm_attributes('-toolwindow', 'True')
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    messagebox.showerror(title, message, parent=root)
    root.destroy()

def show_warning(title: str, message: str) -> None:
    root = tk.Tk()
    root.wm_attributes('-toolwindow', 'True')
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    messagebox.showwarning(title, message, parent=root)
    root.destroy()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convert_encoding(file_path, from_encoding, to_encoding):
    with codecs.open(file_path, 'r', from_encoding) as file:
        content = file.read()
    with codecs.open(file_path, 'w', to_encoding) as file:
        file.write(content)

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
 
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

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
    if vv.parse(now_version) < vv.parse(get_latest_version()):
        return True
    return False

def get_updates():
    if check_update(version):
        show_warning("업데이트", f"새로운 업데이트가 있습니다. 업데이트를 진행합니다.")
        os.startfile(f"updater.exe")
        window.destroy()
    else:
        show_message("업데이트", f"현재 최신 버전입니다.")

def get_unicode(string: str):
    result = ""
    for i in motd:
        if i == " ":
            result += " "
            continue
        if i.encode().isalpha():
            result += i
            continue
        if i.encode().isdigit():
            result += i
            continue
        result += r'\u' + format((ord(i)), "04x")
    return result

def config_create():
    config = cp.ConfigParser()

    config['Settings'] = {}
    config['Settings']['dir'] = ''
    config['Settings']['name'] = '{번호}. {버전}_{버킷}_버킷'

    with open('config.ini', 'w', encoding='UTF-8') as f:
        config.write(f)
    return True

def config_read(key: str):
    if os.path.exists('config.ini') == False:
        config_create()
    config = cp.ConfigParser()
    try: config.read('config.ini', encoding='UTF-8')
    except UnicodeDecodeError as e:
        with open('config.ini', "rb") as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']

            if encoding and not 'utf-8' in encoding.lower():
                contents = content.decode(encoding)
                with open('config.ini', 'w', encoding='UTF-8', newline='\n') as f2:
                    f2.write(contents)
                f2.close()
            f.close()
        config.read('config.ini', encoding='UTF-8')

    try:
        value = config['Settings'][key]
    except KeyError:
        raise KeyError(f'Key "{key}" not found in config.ini')

    return value

def config_write(key: str, value: str):
    if os.path.exists('config.ini') == False:
        config_create()
    config = cp.ConfigParser()
    try: config.read('config.ini', encoding='UTF-8')
    except UnicodeDecodeError as e:
        with open('config.ini', "rb") as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']
            
            if encoding and not 'utf-8' in encoding.lower():
                contents = content.decode(encoding)
                with open('config.ini', 'w', encoding='UTF-8', newline='\n') as f2:
                    f2.write(contents)
                f2.close()
            f.close()
        config.read('config.ini', encoding='UTF-8')

    config['Settings'][key] = value

    with open('config.ini', 'w', encoding='UTF-8') as f:
        config.write(f)

    return True

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def load_properties(file_path):
    properties = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                properties[key] = value
    return properties

def save_properties(file_path, properties):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key, value in properties.items():
            file.write(f'{key}={value}\n')

def modify_property(file_path, key, new_value):
    properties = load_properties(file_path)
    if key in properties:
        properties[key] = new_value
        save_properties(file_path, properties)
    else:
        return False

def download(url, dir, file_name):
    with open(f'{dir}/{file_name}', 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def open_dir():
    dr = filedialog.askdirectory(parent=window,initialdir="/",title='버킷이 생성 될 경로를 선택해주세요.')
    window.focus()
    if dr != "":
        get_bukkit.config(state=tk.NORMAL)
        dir_path.config(state='normal')
        dir_path.delete(0, tk.END)
        dir_path.insert(0, dr)
        dir_path.config(state='readonly')
        config_write('dir', dr)

def open_map_folder():
    global map_folder
    dr = filedialog.askdirectory(parent=window,initialdir="/",title='맵 폴더 경로를 선택해주세요.')
    etc_settings_ui.focus()
    if dr != "":
        map_folder_path.config(state=tk.NORMAL)
        map_folder_path.delete(0, tk.END)
        map_folder_path.insert(0, dr)
        map_folder_path.config(state='readonly')
        map_folder = dr

def open_dir2():
    dr = filedialog.askdirectory(parent=window,initialdir="/",title='자바 폴더 경로를 선택해주세요.')
    window.focus()
    if dr != "":
        java_dir_path.config(state='normal')
        java_dir_path.delete(0, tk.END)
        java_dir_path.insert(0, dr)

def clear_dir():
    java_dir_path.config(state='normal')
    java_dir_path.delete(0, tk.END)
    java_dir_path.insert(0, "(자동 탐지)")
    java_dir_path.config(state='readonly')

def folder_name_resetf():
    folder_name_entry.delete(0, tk.END)
    folder_name_entry.insert(0, "{번호}. {버전}_{버킷}_버킷")
    config_write('name', "{번호}. {버전}_{버킷}_버킷")

def folder_name_savef():
    config_write('name', folder_name_entry.get())

def clear_map_dir():
    global map_folder
    map_folder_path.config(state='normal')
    map_folder_path.delete(0, tk.END)
    map_folder_path.insert(0, "(자동 생성)")
    map_folder = ""
    map_folder_path.config(state='readonly')

def create_thread() -> None:
    '''버킷 제작 버튼 클릭 시 호출, create 함수 스레드로 실행'''
    thread = threading.Thread(target=create)
    thread.daemon = True
    thread.start()

def p_var_update(progress: int) -> None:
    '''프로그레스 바 업데이트'''
    p_var.set(progress)
    progress_bar.update()

def create():
    p_var_update(0)

    # 설정 변수 불러오기
    try:
        selected_bukkit = bukkit_genre.get()
        selected_version = bukkit_version.get()
        selected_build = bukkit_build_v.get()
        selected_min_ram = min_ram_box.get()
        selected_max_ram = max_ram_box.get()
        selected_dir = dir_path.get()
        selected_java = java_dir_path.get()
    except Exception as e: raise(e)

    p_var_update(10)
    # 폴더 생성
    print(selected_bukkit, selected_version, selected_build, selected_min_ram, selected_max_ram, selected_dir)
    progress_text.config(text="폴더 생성 중 . (1/3) | 폴더 개수 확인")
    folder_count = len([name for name in os.listdir(selected_dir) if not os.path.isfile(os.path.join(selected_dir, name))])
    
    progress_text.config(text="폴더 생성 중 .. (2/3) | 폴더 경로 생성")
    dir_path_2 = f'{selected_dir}/{folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}'
    
    progress_text.config(text="폴더 생성 중 ... (3/3) | 폴더 생성")
    os.mkdir(dir_path_2)

    progress_text.config(text="폴더 생성 완료")

    p_var_update(20)
    # 버킷 파일 다운로드
    progress_text.config(text="버킷 파일 다운로드 중 . (1/2) | 버킷 코어 사이트 설정")
    if selected_bukkit == "Paper": url = f'https://api.papermc.io/v2/projects/paper/versions/{selected_version}/builds/{selected_build}/downloads/paper-{selected_version}-{selected_build}.jar'
    elif selected_bukkit == "Folia": url = f'https://api.papermc.io/v2/projects/folia/versions/{selected_version}/builds/{selected_build}/downloads/folia-{selected_version}-{selected_build}.jar'
    elif selected_bukkit == "Velocity": url = f'https://api.papermc.io/v2/projects/velocity/versions/{selected_version}/builds/{selected_build}/downloads/velocity-{selected_version}-{selected_build}.jar'
    elif selected_bukkit == "Leaves": url = f'https://api.leavesmc.org/v2/projects/leaves/versions/{selected_version}/builds/{selected_build}/downloads/leaves-{selected_version}-{selected_build}.jar'
    elif selected_bukkit == "Purpur": url = f'https://api.purpurmc.org/v2/purpur/{selected_version}/{selected_build}/download'
    elif selected_bukkit == "Vanilla":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]

        for i in versions:
            if i['id'] == selected_version:
                url = i["url"]
                break
        
        response = requests.get(url, headers=headers)
        response_json = response.json()
        url = response_json["downloads"]["server"]["url"] 
    elif selected_bukkit == "Forge": url = f'https://maven.minecraftforge.net/net/minecraftforge/forge/{selected_version}-{selected_build}/forge-{selected_version}-{selected_build}-installer.jar'
    elif selected_bukkit == "Fabric":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://meta.fabricmc.net/v2/versions/installer', headers=headers)
        response_json = response.json()
        installer_version = []

        for i in range(len(response_json)):
            installer_version.append(response_json[i]["version"])
        installer_version.sort(reverse=True, key=Version)
        # print(installer_version)
        url = f'https://meta.fabricmc.net/v2/versions/loader/{selected_version}/{selected_build}/{installer_version[0]}/server/jar'
    elif selected_bukkit == "Mohist": url = f"https://mohistmc.com/api/v2/projects/mohist/{selected_version}/builds/{selected_build}/download"
    elif selected_bukkit == "NeoForge": url = f'https://maven.neoforged.net/releases/net/neoforged/neoforge/{selected_build}/neoforge-{selected_build}-installer.jar'
    elif selected_bukkit == "Plazma":
        if selected_version.split(".")[1] == "19" or (selected_version.split(".")[1] == "20" and (selected_version.split(".")[2] == "1" or selected_version.split(".")[2] == "2")):
            url = f'https://dl.plazmamc.org/{selected_version}/1'
        elif selected_version.split(".")[1] == "21" and selected_version.split(".")[2] == "4":
            url = f'https://ci.codemc.io/job/PlazmaMC/job/Plazma/job/dev%252F1.21.4/lastSuccessfulBuild/artifact/build/libs/plazma-paperclip-1.21.4-R0.1-SNAPSHOT-mojmap.jar'
        else:
            url = f'https://dl.plazmamc.org/{selected_version}'
    elif selected_bukkit == "CatServer":
        if selected_version == "1.18.2": url = f'https://catmc.org/download/catserver_1_18_2'
        elif selected_version == "1.16.5": url = f'https://catmc.org/download/catserver_1_16_5'
        elif selected_version == "1.12.2": url = f'https://catserver.moe/download/universal'
    elif selected_bukkit == "Arclight":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get(f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{selected_version}', headers=headers)
        response_json = response.json()
        versions = []
        for i in response_json['files']:
            if i['name'] == 'loaders':
                response2 = requests.get(i['link'], headers=headers)
                break

        response2_json = response2.json()
        for i in response2_json['files']:
            if i['name'] == selected_build:
                response3 = requests.get(i['link'], headers=headers)
                break

        response3_json = response3.json()
        for i in response3_json['files']:
            if i['name'] == 'latest-snapshot':
                url = i['link']
                break
    elif selected_bukkit == "Pufferfish":
        url = f"https://ci.pufferfish.host/job/Pufferfish-1.{selected_version.split('.')[1]}/lastSuccessfulBuild/artifact/build/libs/pufferfish-paperclip-{selected_version}-R0.1-SNAPSHOT-mojmap.jar"
    elif selected_bukkit == "SpongeVanilla":
        url = f"https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongevanilla/{selected_build}/spongevanilla-{selected_build}-universal.jar"

    progress_text.config(text="버킷 파일 다운로드 중 .. (2/2) | 다운로드 중")
    if selected_bukkit == "Forge" or selected_bukkit == "NeoForge": download(url, dir_path_2, f'install.jar')
    else: download(url, dir_path_2, f'server.jar')
    progress_text.config(text="버킷 파일 다운로드 완료")

    p_var_update(30)
    # 자바 경로 설정
    progress_text.config(text="자바 버전 탐지 중 . (1/5) | 자동 탐지 여부 확인")

    if selected_java == "(자동 탐지)":
        progress_text.config(text="자바 버전 탐지 중 .. (2/5) | 자바 폴더 자동 탐지 중")
        if os.path.exists(f'C:/Program Files/Java'): java_path = 'C:/Program Files/Java'
        elif os.path.exists(f'C:/Program Files (x86)/Java'): java_path = 'C:/Program Files (x86)/Java'
        else: return show_error("Error", "자바가 탐지되지 않았습니다. 수동으로 자바 경로를 지정해주세요.")
    else:
        progress_text.config(text="자바 버전 탐지 중 .. (2/5) | 자바 폴더 경로 확인 중")
        if 'java.exe' in selected_java: java_path = selected_java.split('/bin/java.exe')[0]
        else: java_path = selected_java
    progress_text.config(text="자바 버전 탐지 중 ... (3/5) | 자바 폴더 경로 설정")
    

    progress_text.config(text="자바 버전 탐지 중 . (4/5) | 폴더 내 자바 버전 탐지")
    java_version = os.listdir(java_path)

    try:
        if int(selected_version.split('.')[1]) <= 16:
            for i in java_version:
                if '1.8.0' in i:
                    java_version = i
                    break
        elif int(selected_version.split('.')[1]) <= 20:
            try: int(selected_version.split('.')[2])
            except: selected_version += ".0"
            if int(selected_version.split('.')[2]) >= 5:
                for i in java_version:
                    if int(i.split('-')[1]) >= 21:
                        java_version = i
                        break
            else:
                for i in java_version:
                    if int(i.split('-')[1]) >= 17:
                        java_version = i
                        break
        else:
            for i in java_version:
                if int(i.split('-')[1]) >= 21:
                    java_version = i
                    break
    except: java_version = 'java'

    progress_text.config(text="자바 버전 탐지 중 .. (5/5) | 자바 파일 경로 설정")
    java_path = f'{java_path}/{java_version}/bin/java.exe'

    progress_text.config(text="자바 버전 탐지 완료")

    p_var_update(40)
    # 실행 파일 생성
    progress_text.config(text="실행 파일 생성 중 . (1/1) | 실행 파일 생성 중")
    with open(f'{dir_path_2}/start.bat', 'w+') as f:
        if java_version == 'java':
            if selected_bukkit == "Forge" and int(selected_version.split(".")[1]) >= 17:
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\njava -Xms{selected_min_ram} -Xmx{selected_max_ram} @libraries/net/minecraftforge/forge/{selected_version}-{selected_build}/win_args.txt %* nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
            elif selected_bukkit == "NeoForge":
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\njava -Xms{selected_min_ram} -Xmx{selected_max_ram} @libraries/net/neoforged/neoforge/{selected_build}/win_args.txt %* nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
            else:
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\njava -Xms{selected_min_ram} -Xmx{selected_max_ram} -jar server.jar nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
        else:
            if selected_bukkit == "Forge" and int(selected_version.split(".")[1]) >= 17:
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\n"{java_path}" -Xms{selected_min_ram} -Xmx{selected_max_ram} @libraries/net/minecraftforge/forge/{selected_version}-{selected_build}/win_args.txt %* nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
            elif selected_bukkit == "NeoForge":
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\n"{java_path}" -Xms{selected_min_ram} -Xmx{selected_max_ram} @libraries/net/neoforged/neoforge/{selected_build}/win_args.txt %* nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
            else:
                f.write(f'@echo off\ntitle {folder_name_entry.get().replace("{버전}", selected_version).replace("{버킷}", selected_bukkit).replace("{번호}", str(folder_count+1)).replace("{빌드}", selected_build)}\n:main\ncls\n"{java_path}" -Xms{selected_min_ram} -Xmx{selected_max_ram} -jar server.jar nogui\nTIMEOUT 10 /NOBREAK\ngoto main')
        f.close()
    progress_text.config(text="실행 파일 생성 완료")

    if selected_bukkit == "Forge" or selected_bukkit == "NeoForge":
        progress_text.config(text="(Neo)Forge 실행 파일 생성 중 . (1/1) | 실행 파일 생성 중")
        os.chdir(dir_path_2)
        if java_version == 'java':
            os.system(f'java -jar install.jar --installServer')
        else:
            os.system(fr'""{java_path}" -jar install.jar" --installServer')
        os.remove(f'install.jar')
        if int(selected_version.split(".")[1]) <= 16:
            for i in os.listdir(dir_path_2):
                if 'forge-' in i and '.jar' in i:
                    os.rename(i, 'server.jar')
                    break
        else: pass
        progress_text.config(text="(Neo)Forge 실행 파일 생성 완료")

    p_var_update(50)
    # 생성 파일 삭제
    progress_text.config(text="기타 생성 파일 삭제 중 . (1/2) | run.bat 탐지 및 삭제 중")
    if os.path.exists(f'{dir_path_2}/run.bat'): os.remove(f'{dir_path_2}/run.bat')
    progress_text.config(text="기타 생성 파일 삭제 중 . (2/2) | run.bat 탐지 및 삭제 중")
    if os.path.exists(f'{dir_path_2}/run.sh'): os.remove(f'{dir_path_2}/run.sh')
    progress_text.config(text="기타 생성 파일 삭제 완료")

    p_var_update(60)
    # eula 허용
    if not (selected_bukkit == "Mohist" or selected_bukkit == "CatServer"):
        progress_text.config(text="Eula 허용 중 . (1/5) | 버킷 폴더 경로 지정")
        os.chdir(dir_path_2)

        progress_text.config(text="Eula 허용 중 .. (2/5) | 서버 실행 중")
        if java_version == 'java':
            if selected_bukkit == "Forge" and int(selected_version.split(".")[1]) >= 17:
                os.system(f'java @libraries/net/minecraftforge/forge/{selected_version}-{selected_build}/win_args.txt %* nogui')
            elif selected_bukkit == "NeoForge":
                os.system(f'java @libraries/net/neoforged/neoforge/{selected_build}/win_args.txt %* nogui')
            else:
                os.system(f'java -jar server.jar nogui')
        else:
            if selected_bukkit == "Forge" and int(selected_version.split(".")[1]) >= 17:
                os.system(f'"{java_path}" @libraries/net/minecraftforge/forge/{selected_version}-{selected_build}/win_args.txt %* nogui')
            elif selected_bukkit == "NeoForge":
                os.system(f'"{java_path}" @libraries/net/neoforged/neoforge/{selected_build}/win_args.txt %* nogui')
            else:
                os.system(f'"{java_path}" -jar server.jar nogui')

        progress_text.config(text="Eula 허용 중 ... (3/5) | eula.txt 읽기 중")
        with open(f'{dir_path_2}/eula.txt', 'r') as f:
            eula = f.read()
            f.close()

        progress_text.config(text="Eula 허용 중 . (4/5) | 허용 중")
        eula = eula.replace('false', 'true')

        progress_text.config(text="Eula 허용 중 .. (5/5) | eula.txt 쓰기 중")
        with open(f'{dir_path_2}/eula.txt', 'w') as f:
            f.write(eula)
            f.close()

        progress_text.config(text="Eula 허용 완료")

    p_var_update(70)
    # server.properties 수정
    if server_f_status == True:
        progress_text.config(text="server.properties 수정 중 . (1/1) | 수정 중")
        modify_property(f'{dir_path_2}/server.properties', 'gamemode', gamemodes_en[gamemode])
        modify_property(f'{dir_path_2}/server.properties', 'difficulty', difficulties_en[difficulty])
        modify_property(f'{dir_path_2}/server.properties', 'level-type', leveltypes_en[level_type])
        modify_property(f'{dir_path_2}/server.properties', 'pvp', str(pvp).lower())
        modify_property(f'{dir_path_2}/server.properties', 'spawn-protection', str(spawn_protection))
        modify_property(f'{dir_path_2}/server.properties', 'allow-flight', str(allow_flight).lower())
        modify_property(f'{dir_path_2}/server.properties', 'max-players', str(max_players))
        modify_property(f'{dir_path_2}/server.properties', 'enable-command-block', str(allow_command_block).lower())
        modify_property(f'{dir_path_2}/server.properties', 'server-port', str(port))
        modify_property(f'{dir_path_2}/server.properties', 'white-list', str(whitelist).lower())
        modify_property(f'{dir_path_2}/server.properties', 'motd', f'{get_unicode(motd).strip()}')
        progress_text.config(text="server.properties 수정 완료")

    p_var_update(80)
    # 플러그인 다운로드
    if plugins_status == True:
        progress_text.config(text=f"플러그인 다운로드 중 . (1/{len(plugins) + 1}) | 플러그인 폴더 생성")
        if not os.path.exists(f'{dir_path_2}/plugins'):
            os.mkdir(f'{dir_path_2}/plugins')

        _t = '.'
        for i in plugins:
            _t += '.'
            if _t == '...': _t = '.'
            progress_text.config(text=f"플러그인 다운로드 중 .{_t} (1/{len(plugins) + 1}) | ({len(plugins)} 개 중 {plugins.index(i) + 1} 번째) {i[0]} 다운로드 중 ...")
            if i[2] == False:
                url = download_plugins_mods(i[5])
                download(url, f'{dir_path_2}/plugins', str(url).split('/')[-1])
            else: su.copy(i[3], f'{dir_path_2}/plugins/{i[0]}')
        progress_text.config(text=f"플러그인 다운로드 완료")

    p_var_update(90)  
    # 모드 다운로드
    if mods_status == True:
        progress_text.config(text=f"모드 다운로드 중 . (1/{len(mods) + 1}) | 모드 폴더 생성")
        if not os.path.exists(f'{dir_path_2}/mods'):
            os.mkdir(f'{dir_path_2}/mods')

        _t = '.'
        for i in mods:
            _t += '.'
            if _t == '...': _t = '.'
            progress_text.config(text=f"모드 다운로드 중 .{_t} ({mods.index(i) + 2}/{len(mods) + 1}) | ({len(mods)} 개 중 {mods.index(i) + 1} 번째) {i[0]} 다운로드 중 ...")
            if i[2] == False:

                loader = ""
                if selected_bukkit == "NeoForge": loader = "neoforge"
                elif selected_bukkit == "Mohist" or selected_bukkit == "Forge" or selected_bukkit == "CatServer": loader = "forge"
                elif selected_bukkit == "Fabric": loader = "fabric"
                elif selected_bukkit == "Arclight":
                    if selected_build == "neoforge": loader == "neoforge"
                    elif selected_build == "forge": loader = "forge"
                    else: loader = "fabric"

                url = download_plugins_mods(i[5])
                download(url, f'{dir_path_2}/mods', str(url).split('/')[-1])
            else: su.copy(i[3], f'{dir_path_2}/mods/{i[0]}')

            progress_text.config(text=f"모드 다운로드 완료")

    p_var_update(99)
    # 맵 설정
    if map_folder != "":
        progress_text.config(text="맵 폴더 복사 중 . (1/1) | 복사 중")
        # if not os.path.exists(f'{dir_path_2}/world'):
        #     os.mkdir(f'{dir_path_2}/world')
        su.copytree(map_folder, f'{dir_path_2}/world')

        progress_text.config(text="맵 폴더 복사 완료")

    p_var_update(100)
    progress_text.config(text="버킷 생성 완료!")
    print("완료")
    os.startfile(dir_path_2)
    os.chdir(original_dir)

def define_bukkit():
    try:
        selected_bukkit = bukkit_box.get()
        selected_version = bukkit_version_box.get()
        selected_build = bukkit_build_text.get()
    except: return
    global server_f_status
    global plugins_status
    global mods_status
    plugins_status = False
    mods_status = False
    server_f_status = True

    new_bukkit_gui.destroy()

    bukkit_genre.config(state='normal')
    bukkit_genre.delete(0, tk.END)
    bukkit_genre.insert(0, selected_bukkit)
    bukkit_genre.config(state='readonly')

    bukkit_version.config(state='normal')
    bukkit_version.delete(0, tk.END)
    bukkit_version.insert(0, selected_version)
    bukkit_version.config(state='readonly')

    bukkit_build_v.config(state='normal')
    bukkit_build_v.delete(0, tk.END)
    bukkit_build_v.insert(0, selected_build)
    bukkit_build_v.config(state='readonly')
    
    if selected_bukkit != "" and selected_version != "":
        create_button.config(state=tk.NORMAL)
        # server_propeties_button.config(state=tk.NORMAL)
        etc_server_settings_button.config(state=tk.NORMAL)
        plugins_button.config(state=tk.DISABLED)
        mods_button.config(state=tk.DISABLED)

    if selected_bukkit == "Paper" or selected_bukkit == "Purpur" or selected_bukkit == "Mohist" or selected_bukkit == "Plazma" or selected_bukkit == "CatServer" or selected_bukkit == "Arclight" or selected_bukkit == "Pufferfish" or selected_bukkit == "Folia":
        plugins_button.config(state=tk.NORMAL)
        plugins_status = True

    if selected_bukkit == "Mohist" or selected_bukkit == "NeoForge" or selected_bukkit == "Forge" or selected_bukkit == "CatServer" or (selected_bukkit == "Arclight" and (selected_build == "forge" or selected_build == "neoforge")):
        # server_propeties_button.config(state=tk.DISABLED)
        server_f_status = False

    if selected_bukkit == "Mohist" or selected_bukkit == "NeoForge" or selected_bukkit == "Forge" or selected_bukkit == "CatServer" or selected_bukkit == "Arclight" or selected_bukkit == "Fabric":
        mods_button.config(state=tk.NORMAL)
        mods_status = True

def get_build_version_thread(event) -> None:
    '''MC 버전 (콤보 박스) 선택 시 호출, get_build_version 함수 실행하기 위한 쓰레드 생성'''

    bukkit_version_box.selection_clear()

    bukkit_build_text.state(["!disabled"])
    bukkit_build_text.set('불러 오는 중')
    bukkit_build_text.state(["disabled"])

    thread = threading.Thread(target=get_build_version, args=(event,))
    thread.daemon = True
    thread.start()

def get_build_version(event) -> None:
    '''선택한 버킷과 MC 버전에 맞는 빌드를 불러온 후 반영'''

    selected_bukkit = bukkit_box.get()
    selected_version = bukkit_version_box.get()

    if selected_bukkit == "Paper":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/paper/versions/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json["builds"]
        builds.sort(reverse=True)

    if selected_bukkit == "Folia":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/folia/versions/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json["builds"]
        builds.sort(reverse=True)

    if selected_bukkit == "Velocity":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/velocity/versions/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json["builds"]
        builds.sort(reverse=True)

    if selected_bukkit == "Leaves":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.leavesmc.org/v2/projects/leaves/versions/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json["builds"]
        builds.sort(reverse=True)

    elif selected_bukkit == "Purpur":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.purpurmc.org/v2/purpur/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json["builds"]["all"]
        builds.sort(reverse=True)

    elif selected_bukkit == "Vanilla" or selected_bukkit == "Plazma" or selected_bukkit == "CatServer" or selected_bukkit == "Pufferfish":
        builds = []

    elif selected_bukkit == "Forge":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml', headers=headers)
        response_json = response.text
        response_dict = xmltodict.parse(response_json)
        builds = response_dict["metadata"]["versioning"]["versions"]["version"]
        builds = list(builds)

        for i in builds[:]:
            if i.split('-')[0] != selected_version:
                builds.remove(i)

        for i in range(len(builds)):
            builds[i] = builds[i].split('-')[1]
        builds.sort(reverse=True, key=Version)

    elif selected_bukkit == "Fabric":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://meta.fabricmc.net/v1/versions/loader/{0}'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json
        for i in range(len(builds)):
            builds[i] = builds[i]["loader"]["version"]
        
        for i in builds[:]:
            if int(i.split('.')[1]) < 12:
                builds.remove(i)

    elif selected_bukkit == "Mohist":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://mohistmc.com/api/v2/projects/mohist/{0}/builds'.format(selected_version), headers=headers)
        response_json = response.json()
        builds = response_json['builds']
        for i in range(len(builds)):
            builds[i] = builds[i]["number"]

        builds.sort(reverse=True)

    elif selected_bukkit == "NeoForge":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge', headers=headers)
        response_json = response.json()
        builds = []
        for i in response_json['versions']:
            if i.split('.')[0] == selected_version.split('.')[1] and i.split('.')[1] == selected_version.split('.')[2]:
                builds.append(i)
        builds.sort(reverse=True, key=Version)

    elif selected_bukkit == "Arclight":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get(f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{selected_version}', headers=headers)
        response_json = response.json()
        builds = []
        for i in response_json['files']:
            if i['name'] == 'loaders':
                response2 = requests.get(i['link'], headers=headers)
                break

        response2_json = response2.json()
        for i in response2_json['files']:
            builds.append(i['name'])

    elif selected_bukkit == "SpongeVanilla":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get(f'https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts/spongevanilla/versions?tags=,minecraft:{selected_version}', headers=headers)
        response_json = response.json()
        builds = []
        for i in response_json['artifacts']:
            builds.append(i)

    bukkit_build_text.set('')
    bukkit_build_text.config(values=builds)
    bukkit_build_text.state(["!disabled"])
    bukkit_build_text.state(["readonly"])
    if len(builds) > 0: bukkit_build_text.current(0)
    else: bukkit_build_text.state(["disabled"])

    bukkit_select_button.config(state=tk.NORMAL)

def get_bukkit_version_thread(event) -> None:
    '''버킷 종류 (콤보 박스) 선택 시 호출, get_bukkit_version 함수 실행하기 위한 쓰레드 생성'''

    bukkit_box.selection_clear()

    bukkit_select_button.config(state=tk.DISABLED)

    bukkit_build_text.set('')
    bukkit_build_text.state(["disabled"])

    bukkit_version_box.state(["!disabled"])
    bukkit_version_box.set('불러 오는 중')
    bukkit_version_box.state(["disabled"])

    thread = threading.Thread(target=get_bukkit_version, args=(event,))
    thread.daemon = True
    thread.start()

def get_bukkit_version(event):

    selected_bukkit = bukkit_box.get()

    if selected_bukkit == "Paper":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/paper', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "Folia":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/folia', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "Velocity":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.papermc.io/v2/projects/velocity', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions.sort(reverse=True)

    elif selected_bukkit == "Leaves":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.leavesmc.org/v2/projects/leaves', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "Purpur":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://api.purpurmc.org/v2/purpur', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "Vanilla":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]
        versions = [version["id"] for version in versions]

    elif selected_bukkit == "Forge":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json', headers=headers)
        response_json = response.json()
        versions = response_json["promos"]
        versions = list(versions.keys())
        for i in range(len(versions)):
            versions[i] = versions[i].split('-')[0]
        versions = list(set(versions))
        versions.sort(reverse=True, key=Version)
        
    elif selected_bukkit == "Fabric":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://meta.fabricmc.net/v2/versions/game', headers=headers)
        response_json = response.json()
        versions = response_json
        for i in range(len(versions)):
            versions[i] = versions[i]["version"]
        
    elif selected_bukkit == "Mohist":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://mohistmc.com/api/v2/projects/mohist', headers=headers)
        response_json = response.json()
        versions = response_json["versions"]

        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "NeoForge":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge', headers=headers)
        response_json = response.json()
        versions = []
        for i in response_json['versions']:
            versions.append(f"1.{i.split('.')[0]}.{i.split('.')[1]}")
        versions = list(set(versions))
        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "Plazma":
        versions = ["1.21.4", "1.21.3", "1.21.1", "1.20.6", "1.20.4", "1.20.2", "1.20.1", "1.19.4"]

    elif selected_bukkit == "CatServer":
        versions = ["1.18.2", "1.16.5", "1.12.2"]

    elif selected_bukkit == "Pufferfish":
        versions = ["1.21.3", "1.20.4", "1.19.4", "1.18.2", "1.17.1"]

    elif selected_bukkit == "Arclight":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://files.hypoglycemia.icu/v1/files/arclight/minecraft', headers=headers)
        response_json = response.json()
        versions = []
        for i in response_json["files"]:
            versions.append(i["name"])

        versions.sort(reverse=True, key=Version)

    elif selected_bukkit == "SpongeVanilla":
        headers = {
            'accept': 'application/json',
        }

        response = requests.get('https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts/spongevanilla', headers=headers)
        response_json = response.json()
        versions = []
        for i in response_json["tags"]["minecraft"]:
            versions.append(i)
        versions.sort(reverse=True, key=Version)

    bukkit_version_box.set('')
    bukkit_version_box.config(values=versions)

    bukkit_version_box.state(["!disabled"])
    bukkit_version_box.state(["readonly"])

def get_bukkit_info() -> None:
    '''버킷 선택 버튼 클릭 시 호출, 버킷 정보를 불러올 수 있는 하위 GUI (new_bukkit_gui) 오픈'''

    global new_bukkit_gui
    global bukkit_list

    try:
        new_bukkit_gui.focus()
        return
    except: pass
    
    new_bukkit_gui = tk.Toplevel(window)
    new_bukkit_gui.title("")
    new_bukkit_gui.minsize(new_bukkit_gui.winfo_width(), new_bukkit_gui.winfo_height())
    new_bukkit_gui.resizable(False, False)

    new_bukkit_gui.wm_attributes("-topmost", 1)

    new_bukkit_gui.update()
    new_bukkit_gui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    apply_theme_to_titlebar(new_bukkit_gui)

    global main_frame_2
    main_frame_2 = ttk.LabelFrame(new_bukkit_gui, text="Bukkit", padding=(20, 10))
    main_frame_2.config(labelanchor='n')
    main_frame_2.grid(row=0, column=0, padx=10, pady=10)

    bukkit_version_list = []
    bukkit_build_list = []

    bukkit_label = tk.Label(main_frame_2, text="버킷 종류")
    bukkit_label.grid(row=0, column=0, padx=5, pady=5)

    global bukkit_box
    bukkit_box = ttk.Combobox(main_frame_2, width=10, values=bukkit_list, state="readonly")
    bukkit_box.current()
    bukkit_box.bind("<<ComboboxSelected>>", get_bukkit_version_thread)
    bukkit_box.grid(row=0, column=1, padx=5, pady=5)

    bukkit_version_label = tk.Label(main_frame_2, text="버전")
    bukkit_version_label.grid(row=1, column=0, padx=5, pady=5)

    global bukkit_version_box
    bukkit_version_box = ttk.Combobox(main_frame_2, width=10, values=bukkit_version_list, state="disabled")
    bukkit_version_box.bind("<<ComboboxSelected>>", get_build_version_thread)
    bukkit_version_box.grid(row=1, column=1, padx=5, pady=5)

    bukkit_build_label = tk.Label(main_frame_2, text="빌드")
    bukkit_build_label.grid(row=2, column=0, padx=5, pady=5)

    global bukkit_build_text
    bukkit_build_text = ttk.Combobox(main_frame_2, width=10, values=bukkit_build_list, state="disabled")
    bukkit_build_text.bind("<<ComboboxSelected>>", lambda event: bukkit_build_text.selection_clear())
    bukkit_build_text.grid(row=2, column=1, padx=5, pady=5)

    global bukkit_select_button
    bukkit_select_button = ttk.Button(main_frame_2, text="선택", width=10, command=define_bukkit, state="disabled")
    bukkit_select_button.grid(row=3, column=1, padx=5, pady=5)

def download_plugins_mods(id):
    response = requests.get(f'https://api.modrinth.com/v2/version/{id}')
    result = response.json()
    return result['files'][0]['url']

def search_plugins_version(id, versions):
    response = requests.get(f'https://api.modrinth.com/v2/project/{id}/version?loaders=["bukkit", "paper"]&game_versions=["{versions}"]')
    result = response.json()
    results = []
    for i in result:
        results.append([i['id'], i['version_number']])
    return results

def search_mods_version(id, versions, loader):
    if "neoforge" in loader:
        response = requests.get(f'https://api.modrinth.com/v2/project/{id}/version?loaders=["neoforge"]&game_versions=["{versions}"]')
    elif "forge" in loader:
        response = requests.get(f'https://api.modrinth.com/v2/project/{id}/version?loaders=["forge"]&game_versions=["{versions}"]')
    elif "fabric" in loader:
        response = requests.get(f'https://api.modrinth.com/v2/project/{id}/version?loaders=["fabric"]&game_versions=["{versions}"]')
    result = response.json()
    results = []
    for i in result:
        results.append([i['id'], i['version_number']])
    return results

def search_plugin(query: str, versions: str):
    response = requests.get(f'https://api.modrinth.com/v2/search?query={query}&facets=[["categories:bukkit","categories:paper"],["project_type:plugin"],["versions:{versions}"]]&limit=20')
    result = response.json()
    results = []
    for i in result['hits']:
        results.append([i['project_id'], i['title'], i['description'], i['icon_url']])
    return results

def search_mods(query: str, versions: str, loader: str):
    if loader == "neoforge":
        response = requests.get(f'https://api.modrinth.com/v2/search?query={query}&facets=[["categories:neoforge"],["project_type:mod"],["versions:{versions}"],["server_side:optional","server_side:required"]]&limit=20')
    elif loader == "forge":
        response = requests.get(f'https://api.modrinth.com/v2/search?query={query}&facets=[["categories:forge"],["project_type:mod"],["versions:{versions}"],["server_side:optional","server_side:required"]]&limit=20')
    elif loader == "fabric":
        response = requests.get(f'https://api.modrinth.com/v2/search?query={query}&facets=[["categories:fabric"],["project_type:mod"],["versions:{versions}"],["server_side:optional","server_side:required"]]&limit=20')
    result = response.json()
    results = []
    for i in result['hits']:
        results.append([i['project_id'], i['title'], i['description'], i['icon_url']])
    return results

def search_append_plugin_thread() -> None:
    '''플러그인 검색 결과 추가를 위한 쓰레드 생성'''
    thread = threading.Thread(target=search_append_plugin)
    thread.daemon = True
    thread.start()

def search_append_plugin():
    query = search_plugin_box.get()
    versions = bukkit_version.get()
    # versions = "1.21.4"

    global get_p
    get_p = search_plugin(query, versions)
    search_plugin_tree.delete(*search_plugin_tree.get_children())

    global images
    images = []
    for i in get_p:
        try:
            u = requests.get(i[3])
            img = Image.open(BytesIO(u.content)).resize((15, 15))
            photo = ImageTk.PhotoImage(img)
            images.append(photo)
        except:
            photo = None
        if photo == None:
            search_plugin_tree.insert("", "end", values=(i[1], i[2]))
        else:
            search_plugin_tree.insert("", "end", values=(i[1], i[2]), image=photo)

def search_append_mods_thread() -> None:
    '''모드 검색 결과 추가를 위한 쓰레드 생성'''
    thread = threading.Thread(target=search_append_mods)
    thread.daemon = True
    thread.start()

def search_append_mods():
    query = search_mods_box.get()
    versions = bukkit_version.get()
    selected_bukkit = bukkit_genre.get()
    selected_build = bukkit_build_v.get()
    # versions = "1.21.4"

    global get_m
    loader = ""
    if selected_bukkit == "NeoForge": loader = "neoforge"
    elif selected_bukkit == "Mohist" or selected_bukkit == "Forge" or selected_bukkit == "CatServer": loader = "forge"
    elif selected_bukkit == "Fabric": loader = "fabric"
    elif selected_bukkit == "Arclight":
        if selected_build == "neoforge": loader == "neoforge"
        elif selected_build == "forge": loader = "forge"
        else: loader = "fabric"

    get_m = search_mods(query=query, versions=versions, loader=loader)
    search_mods_tree.delete(*search_mods_tree.get_children())

    global Mimages
    Mimages = []
    for i in get_m:
        try:
            u = requests.get(i[3])
            img = Image.open(BytesIO(u.content)).resize((15, 15))
            photo = ImageTk.PhotoImage(img)
            Mimages.append(photo)
        except:
            photo = None
        if photo == None:
            search_mods_tree.insert("", "end", values=(i[1], i[2]))
        else:
            search_mods_tree.insert("", "end", values=(i[1], i[2]), image=photo)

def refresh_plugins_thread() -> None:
    '''플러그인 목록 새로고침을 위한 쓰레드 생성'''
    thread = threading.Thread(target=refresh_plugins)
    thread.daemon = True
    thread.start()

def refresh_plugins() -> None:
    '''플러그인 목록 새로고침'''
    plugin_list_tree.delete(*plugin_list_tree.get_children())

    global images
    images = []

    for i in plugins:
        if i[2] == False:
            try:
                u = requests.get(i[4])
                img = Image.open(BytesIO(u.content)).resize((15, 15))
                photo = ImageTk.PhotoImage(img)
                images.append(photo)
            except:
                photo = None
            if photo == None:
                plugin_list_tree.insert("", "end", values=(i[0],i[6]))
            else:
                plugin_list_tree.insert("", "end", values=(i[0],i[6]), image=photo)
        else:
            plugin_list_tree.insert("", "end", values=(i[0],))

    try: remove_plugin_button.config(state=tk.DISABLED)
    except: pass

def refresh_mods_thread() -> None:
    '''모드 목록 새로고침을 위한 쓰레드 생성'''
    thread = threading.Thread(target=refresh_mods)
    thread.daemon = True
    thread.start()

def refresh_mods():
    mods_list_tree.delete(*mods_list_tree.get_children())
    global Mimages
    Mimages = []
    for i in mods:
        if i[2] == False:
            try:
                u = requests.get(i[4])
                img = Image.open(BytesIO(u.content)).resize((15, 15))
                photo = ImageTk.PhotoImage(img)
                Mimages.append(photo)
            except:
                photo = None
            if photo == None:
                mods_list_tree.insert("", "end", values=(i[0],i[6]))
            else:
                mods_list_tree.insert("", "end", values=(i[0],i[6]), image=photo)
        else:
            mods_list_tree.insert("", "end", values=(i[0],))

    try: remove_mod_button.config(state=tk.DISABLED)
    except: pass

def define_plugins_thread() -> None:
    '''플러그인 확정을 위한 쓰레드 생성'''
    plugins_builds_dropbox.state(["!disabled"])
    plugins_builds_dropbox.state(["readonly"])
    plugins_builds_dropbox.set('불러 오는 중')
    plugins_builds_dropbox.state(["disabled"])

    thread = threading.Thread(target=define_plugins)
    thread.daemon = True
    thread.start()

def define_plugins():
    global plugins
    s = get_p[search_plugin_tree.index(search_plugin_tree.selection())]
    global get_b_p
    get_b_p = search_plugins_version(s[0], bukkit_version.get())
    builds = []
    for i in get_b_p:
        builds.append(i[1])
    try: builds.sort(key=Version, reverse=True)
    except: builds.sort(reverse=True)

    plugins_builds_dropbox.set('')
    plugins_builds_dropbox.config(values=builds)
    plugins_builds_dropbox.state(["!disabled"])
    plugins_builds_dropbox.state(["readonly"])
    plugins_builds_dropbox.current(0)

    define_plugins_button.config(state=tk.NORMAL)

def define_plugins2():
    global plugins
    s = get_p[search_plugin_tree.index(search_plugin_tree.selection())]
    build = get_b_p[plugins_builds_dropbox.current()]
    plugins.append([s[1], s[2], False, s[0], s[3], build[0], build[1]])
    plugins_ui.destroy()
    refresh_plugins_thread()

def define_mods2():
    global mods
    s = get_m[search_mods_tree.index(search_mods_tree.selection())]
    build = get_b[mods_builds_dropbox.current()]
    mods.append([s[1], s[2], False, s[0], s[3], build[0], build[1]])
    mods_ui.destroy()
    refresh_mods_thread()

def define_mods_thread() -> None:
    '''모드 확정을 위한 쓰레드 생성'''
    mods_builds_dropbox.state(["!disabled"])
    mods_builds_dropbox.state(["readonly"])
    mods_builds_dropbox.set('불러 오는 중')
    mods_builds_dropbox.state(["disabled"])

    thread = threading.Thread(target=define_mods)
    thread.daemon = True
    thread.start()

def define_mods():
    global mods
    selected_bukkit = bukkit_genre.get()
    selected_build = bukkit_build_v.get()
    s = get_m[search_mods_tree.index(search_mods_tree.selection())]
    loader = ""
    if selected_bukkit == "NeoForge": loader = "neoforge"
    elif selected_bukkit == "Mohist" or selected_bukkit == "Forge" or selected_bukkit == "CatServer": loader = "forge"
    elif selected_bukkit == "Fabric": loader = "fabric"
    elif selected_bukkit == "Arclight":
        if selected_build == "neoforge": loader == "neoforge"
        elif selected_build == "forge": loader = "forge"
        else: loader = "fabric"

    global get_b
    get_b = search_mods_version(s[0], bukkit_version.get(), loader)
    builds = []
    for i in get_b:
        builds.append(i[1])
    try: builds.sort(key=Version, reverse=True)
    except: builds.sort(reverse=True)

    mods_builds_dropbox.set('')
    mods_builds_dropbox.config(values=builds)
    mods_builds_dropbox.state(["!disabled"])
    mods_builds_dropbox.state(["readonly"])
    mods_builds_dropbox.current(0)

    define_mods_button.config(state=tk.NORMAL)

def define_mods2():
    global mods
    s = get_m[search_mods_tree.index(search_mods_tree.selection())]
    build = get_b[mods_builds_dropbox.current()]
    mods.append([s[1], s[2], False, s[0], s[3], build[0], build[1]])
    mods_ui.destroy()
    refresh_mods_thread()

def open_plugins():
    selected_version = bukkit_version.get()
    # selected_version = "1.21.4"
    global plugins_ui

    try:
        plugins_ui.focus()
        return
    except: pass
    plugins_ui = tk.Toplevel(window)
    plugins_ui.title("")
    plugins_ui.minsize(plugins_ui.winfo_width(), plugins_ui.winfo_height())
    plugins_ui.resizable(False, False)

    plugins_ui.wm_attributes("-topmost", 1)

    plugins_ui.update()
    plugins_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    apply_theme_to_titlebar(plugins_ui)

    main_frame = ttk.LabelFrame(plugins_ui, text="Plugins (Modrinth)", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    search_plugin_label = tk.Label(main_frame, text="플러그인 이름")
    search_plugin_label.grid(row=0, column=0, padx=5, pady=5)

    global search_plugin_box
    search_plugin_box = ttk.Entry(main_frame, width=65)
    search_plugin_box.grid(row=0, column=1, padx=5, pady=5)

    search_plugin_button = ttk.Button(main_frame, text="검색", width=5, command=search_append_plugin_thread)
    search_plugin_button.grid(row=0, column=2, padx=5, pady=5)

    global search_plugin_tree
    search_plugin_tree = ttk.Treeview(main_frame, columns=("이름", "설명"), show="tree headings", selectmode="browse")
    search_plugin_tree.column('#0', width=40)
    search_plugin_tree.heading("이름", text="이름")
    search_plugin_tree.heading("설명", text="설명")
    search_plugin_tree.column("이름", width=150)
    search_plugin_tree.column("설명", width=500)
    search_plugin_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    search_plugin_tree.bind('<Motion>', 'break')
    
    def m_c(event) -> None:
        plugins_builds_dropbox.set('')
        plugins_builds_dropbox.state(["disabled"])
        select_plugin_button.config(state=tk.NORMAL)
    search_plugin_tree.bind('<<TreeviewSelect>>', m_c)

    search_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=search_plugin_tree.yview)
    search_scroll.grid(row=1, column=3, sticky='ns')
    search_plugin_tree.configure(yscrollcommand=search_scroll.set)

    select_plugin_button = ttk.Button(main_frame, text="선택", width=5, command=define_plugins_thread, state="disabled")
    select_plugin_button.grid(row=2, column=0, padx=5, pady=5)

    global plugins_builds_dropbox
    plugins_builds_dropbox = ttk.Combobox(main_frame, width=60, values=[], state="disabled")
    plugins_builds_dropbox.grid(row=2, column=1, padx=5, pady=5)

    global define_plugins_button
    define_plugins_button = ttk.Button(main_frame, text="확정", width=5, command=define_plugins2, state="disabled")
    define_plugins_button.grid(row=2, column=2, padx=5, pady=5)

    search_append_plugin_thread()

def open_mods():
    global mods_ui

    try:
        mods_ui.focus()
        return
    except: pass
    mods_ui = tk.Toplevel(window)
    mods_ui.title("")
    mods_ui.minsize(mods_ui.winfo_width(), mods_ui.winfo_height())
    mods_ui.resizable(False, False)

    mods_ui.wm_attributes("-topmost", 1)

    mods_ui.update()
    mods_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    apply_theme_to_titlebar(mods_ui)

    main_frame = ttk.LabelFrame(mods_ui, text="Mods (Modrinth)", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    search_mods_label = tk.Label(main_frame, text="모드 이름")
    search_mods_label.grid(row=0, column=0, padx=5, pady=5)

    global search_mods_box
    search_mods_box = ttk.Entry(main_frame, width=65)
    search_mods_box.grid(row=0, column=1, padx=5, pady=5)

    search_mods_button = ttk.Button(main_frame, text="검색", width=5, command=search_append_mods_thread)
    search_mods_button.grid(row=0, column=2, padx=5, pady=5)

    global search_mods_tree
    search_mods_tree = ttk.Treeview(main_frame, columns=("이름", "설명"), show="tree headings", selectmode="browse")
    search_mods_tree.column('#0', width=40)
    search_mods_tree.heading("이름", text="이름")
    search_mods_tree.heading("설명", text="설명")
    search_mods_tree.column("이름", width=150)
    search_mods_tree.column("설명", width=500)
    search_mods_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    search_mods_tree.bind('<Motion>', 'break')
    def m_c(event) -> None:
        mods_builds_dropbox.set('')
        mods_builds_dropbox.state(["disabled"])
        select_mods_button.config(state=tk.NORMAL)
    search_mods_tree.bind('<<TreeviewSelect>>', m_c)

    search_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=search_mods_tree.yview)
    search_scroll.grid(row=1, column=3, sticky='ns')
    search_mods_tree.configure(yscrollcommand=search_scroll.set)

    select_mods_button = ttk.Button(main_frame, text="선택", width=5, command=define_mods_thread, state="disabled")
    select_mods_button.grid(row=2, column=0, padx=5, pady=5)

    global mods_builds_dropbox
    mods_builds_dropbox = ttk.Combobox(main_frame, width=60, values=[], state="disabled")
    mods_builds_dropbox.bind("<<ComboboxSelected>>", lambda event: mods_builds_dropbox.selection_clear())
    mods_builds_dropbox.grid(row=2, column=1, padx=5, pady=5)

    global define_mods_button
    define_mods_button = ttk.Button(main_frame, text="확정", width=5, command=define_mods2, state="disabled")
    define_mods_button.grid(row=2, column=2, padx=5, pady=5)

    search_append_mods_thread()

def open_cplugins():
    global plugins
    dr = filedialog.askopenfilename(parent=plugins_list_ui, initialdir="/",title='수동으로 추가 할 플러그인을 선택해주세요.')
    if dr != "":
        if not (dr.split('.')[-1] == "jar" or dr.split('.')[-1] == "dll"): return show_error("오류", "올바른 플러그인 파일이 아닙니다.")
        plugins.append([dr.split('/')[-1], "", True, dr, ""])
        refresh_plugins_thread()

def open_cmods():
    global mods
    dr = filedialog.askopenfilename(parent=mods_list_ui, initialdir="/",title='수동으로 추가 할 모드를 선택해주세요.')
    if dr != "":
        if not (dr.split('.')[-1] == "jar" or dr.split('.')[-1] == "dll"): return show_error("오류", "올바른 모드 파일이 아닙니다.")
        mods.append([dr.split('/')[-1], "", True, dr, ""])
        refresh_mods_thread()

def open_plugin_list():
    global plugins_list_ui
    try:
        plugins_list_ui.focus()
        return
    except: pass
    plugins_list_ui = tk.Toplevel(window)
    plugins_list_ui.title("")
    plugins_list_ui.minsize(plugins_list_ui.winfo_width(), plugins_list_ui.winfo_height())
    plugins_list_ui.resizable(False, False)

    plugins_list_ui.wm_attributes("-topmost", 1)

    plugins_list_ui.update()
    plugins_list_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    apply_theme_to_titlebar(plugins_list_ui)

    main_frame = ttk.LabelFrame(plugins_list_ui, text="Plugins", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    global plugin_list_tree
    plugin_list_tree = ttk.Treeview(main_frame, columns=("이름", "빌드"), show="tree headings", selectmode="browse")
    plugin_list_tree.column('#0', width=40)
    plugin_list_tree.heading("이름", text="이름")
    plugin_list_tree.heading("빌드", text="빌드")
    plugin_list_tree.column("이름", width=200)
    plugin_list_tree.column("빌드", width=100)
    plugin_list_tree.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    plugin_list_tree.bind('<Motion>', 'break')
    plugin_list_tree.bind('<<TreeviewSelect>>', lambda event: remove_plugin_button.config(state=tk.NORMAL))

    search_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=plugin_list_tree.yview)
    search_scroll.grid(row=0, column=3, sticky='ns')
    plugin_list_tree.configure(yscrollcommand=search_scroll.set)

    custom_plugins_button = ttk.Button(main_frame, text="추가", width=10, command=open_cplugins)
    custom_plugins_button.grid(row=3, column=0, padx=5, pady=5)

    download_plugin_button = ttk.Button(main_frame, text="검색", width=10, command=open_plugins)
    download_plugin_button.grid(row=2, column=0, padx=5, pady=5)

    def remove_plugins():
        global plugins
        try:
            selected = plugin_list_tree.selection()[0]
            for i in range(len(plugins)):
                if plugins[i][0] == plugin_list_tree.item(selected, 'values')[0]:
                    del plugins[i]
                    break
            refresh_plugins_thread()
        except: pass

    global remove_plugin_button
    remove_plugin_button = ttk.Button(main_frame, text="삭제", width=10, command=remove_plugins, state="disabled")
    remove_plugin_button.grid(row=2, column=1, padx=5, pady=5)

    done_plugin = ttk.Button(main_frame, text="확인", width=10, command=lambda: plugins_list_ui.destroy())
    done_plugin.grid(row=2, column=2, padx=5, pady=5)

    refresh_plugins_thread()

    def close():
        plugins_list_ui.destroy()
        try: plugins_ui.destroy()
        except: pass
    plugins_list_ui.protocol("WM_DELETE_WINDOW", close)

def open_mods_list():
    global mods_list_ui
    try:
        mods_list_ui.focus()
        return
    except: pass
    mods_list_ui = tk.Toplevel(window)
    mods_list_ui.title("")
    mods_list_ui.minsize(mods_list_ui.winfo_width(), mods_list_ui.winfo_height())
    mods_list_ui.resizable(False, False)

    mods_list_ui.wm_attributes("-topmost", 1)

    mods_list_ui.update()
    mods_list_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    apply_theme_to_titlebar(mods_list_ui)

    main_frame = ttk.LabelFrame(mods_list_ui, text="Mods", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    global mods_list_tree
    mods_list_tree = ttk.Treeview(main_frame, columns=("이름", "빌드"), show="tree headings", selectmode="browse")
    mods_list_tree.column('#0', width=40)
    mods_list_tree.heading("이름", text="이름")
    mods_list_tree.heading("빌드", text="빌드")
    mods_list_tree.column("이름", width=200)
    mods_list_tree.column("빌드", width=100)
    mods_list_tree.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    mods_list_tree.bind('<Motion>', 'break')
    mods_list_tree.bind('<<TreeviewSelect>>', lambda event: remove_mod_button.config(state=tk.NORMAL))

    search_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=mods_list_tree.yview)
    search_scroll.grid(row=0, column=3, sticky='ns')
    mods_list_tree.configure(yscrollcommand=search_scroll.set)

    custom_mods_button = ttk.Button(main_frame, text="추가", width=10, command=open_cmods)
    custom_mods_button.grid(row=3, column=0, padx=5, pady=5)

    download_mods_button = ttk.Button(main_frame, text="검색", width=10, command=open_mods)
    download_mods_button.grid(row=2, column=0, padx=5, pady=5)

    def remove_mods():
        global mods
        try:
            selected = mods_list_tree.selection()[0]
            for i in range(len(mods)):
                if mods[i][0] == mods_list_tree.item(selected, 'values')[0]:
                    del mods[i]
                    break
            refresh_mods_thread()
        except: pass

    global remove_mod_button
    remove_mod_button = ttk.Button(main_frame, text="삭제", width=10, command=remove_mods, state="disabled")
    remove_mod_button.grid(row=2, column=1, padx=5, pady=5)

    done_mods = ttk.Button(main_frame, text="확인", width=10, command=lambda: mods_list_ui.destroy())
    done_mods.grid(row=2, column=2, padx=5, pady=5)

    refresh_mods_thread()

    def close():
        mods_list_ui.destroy()
        try: mods_ui.destroy()
        except: pass
    mods_list_ui.protocol("WM_DELETE_WINDOW", close)

def motd_change_preview(event):
    motd_preview.config(state='normal')
    motd_preview.delete('1.0', tk.END)
    content = motd_box.get("1.0", tk.END)
    
    # 마인크래프트 색상 코드 및 스타일 매핑
    color_codes = {
        '0': 'black', '1': 'blue', '2': 'green', '3': 'cyan', '4': 'red', '5': 'magenta', '6': 'yellow', '7': 'white',
        '8': 'gray', '9': 'lightblue', 'a': 'lightgreen', 'b': 'lightcyan', 'c': 'lightcoral', 'd': 'pink', 'e': 'lightyellow', 'f': 'white'
    }
    style_codes = {
        'l': {'font': (font_f, 10, 'bold')},
        'o': {'font': (font_f, 10, 'italic')},
        'n': {'underline': True},
        'm': {'overstrike': True},
        'k': {'font': ('Helvetica', 10, 'overstrike')},
        'r': {}
    }

    pattern = re.compile(r'(§.)')
    segments = pattern.split(content)
    current_tags = []
    for segment in segments:
        if segment.startswith('§') and len(segment) > 1:
            code = segment[1]
            if code == 'r':
                current_tags.clear()
            elif code in color_codes:
                current_tags.append(f'color{code}')
                motd_preview.tag_config(f'color{code}', foreground=color_codes[code])
            elif code in style_codes:
                if code == 'r':
                    current_tags.clear()
                else:
                    current_tags.append(f'style{code}')
                    motd_preview.tag_config(f'style{code}', **style_codes[code])
        else:
            motd_preview.insert(tk.END, segment, tuple(current_tags))
            
    motd_preview.config(state='disabled')

def motd_color_set(event):
    selected_color = motd_color_box.get()
    if motd_color.index(selected_color) < 10:
        motd_box.insert(tk.INSERT, f"§{motd_color.index(selected_color)}")
    else:
        motd_box.insert(tk.INSERT, f"§{chr(motd_color.index(selected_color) + 87)}")
    motd_change_preview(None)

def etc_settings():
    global etc_settings_ui
    try:
        etc_settings_ui.focus()
        return
    except: pass
    etc_settings_ui = tk.Toplevel(window)
    etc_settings_ui.title("")
    etc_settings_ui.minsize(etc_settings_ui.winfo_width(), etc_settings_ui.winfo_height())
    etc_settings_ui.resizable(False, False)

    etc_settings_ui.wm_attributes("-topmost", 1)

    apply_theme_to_titlebar(etc_settings_ui)

    etc_settings_ui.update()
    etc_settings_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    # main_text = tk.Label(detail_settings_ui, text="서버 설정", font=(font_f, "15"))
    # main_text.grid(row=0, column=1, pady=10)

    main_frame = ttk.LabelFrame(etc_settings_ui, text="Settings", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    etc_settings_apply_button = ttk.Button(etc_settings_ui, text="적용", width=10, command=lambda: etc_settings_ui.destroy())
    etc_settings_apply_button.grid(row=0, column=1, padx=5)

    if server_f_status is True:
        server_propeties_button = ttk.Button(main_frame, text="server.propeties", width=25, command=detail_settings)
    else:
        server_propeties_button = ttk.Button(main_frame, text="server.propeties", width=25, command=detail_settings, state=tk.DISABLED)
    server_propeties_button.grid(row=1, column=1, pady=5)

    global detail_settings_text
    detail_settings_text = tk.Label(main_frame, text="서버 설정")
    detail_settings_text.grid(row=2, column=1, pady=5)
    if server_f_status is True:
        detail_settings_text.config(text=f"게임모드: {gamemodes[gamemode]}\n난이도: {difficulties[difficulty]}\n레벨 타입: {leveltypes[level_type]}\nPvP: {pvp}\n스폰 보호: {spawn_protection}\n비행 허용: {allow_flight}\n최대 플레이어 수: {max_players}\n커맨드 블록 허용: {allow_command_block}\n포트: {port}\n화이트리스트: {whitelist}\nMOTD: {motd}")
    else:
        detail_settings_text.config(text="")

    map_folder_label = tk.Label(main_frame, text="맵 폴더")
    map_folder_label.grid(row=0, column=0, padx=5, pady=5)

    global map_folder_path
    map_folder_path = ttk.Entry(main_frame, width=25, font=font)
    map_folder_path.insert(0, f"{'(자동 생성)' if map_folder == '' else map_folder}")
    map_folder_path.config(state='readonly')
    map_folder_path.grid(row=0, column=1, padx=5, pady=5)

    map_folder_open_button = ttk.Button(main_frame, text="열기", width=5, command=open_map_folder)
    map_folder_open_button.grid(row=0, column=2, padx=5, pady=5)

    map_folder_clear_button = ttk.Button(main_frame, text="초기화", width=5, command=clear_map_dir)
    map_folder_clear_button.grid(row=0, column=3, padx=0, pady=5)

    def close():
        etc_settings_ui.destroy()
        try: detail_settings_ui.destroy()
        except: pass
    etc_settings_ui.protocol("WM_DELETE_WINDOW", close)
    
def detail_settings():
    global detail_settings_ui
    try:
        detail_settings_ui.focus()
        return
    except: pass
    detail_settings_ui = tk.Toplevel(window)
    detail_settings_ui.title("")
    detail_settings_ui.minsize(detail_settings_ui.winfo_width(), detail_settings_ui.winfo_height())
    detail_settings_ui.resizable(False, False)

    detail_settings_ui.wm_attributes("-topmost", 1)

    apply_theme_to_titlebar(detail_settings_ui)

    detail_settings_ui.update()
    detail_settings_ui.geometry(f"+{window.winfo_x()}+{window.winfo_y()}")

    # main_text = tk.Label(detail_settings_ui, text="서버 설정", font=(font_f, "15"))
    # main_text.grid(row=0, column=1, pady=10)

    main_frame = ttk.LabelFrame(detail_settings_ui, text="Settings", padding=(20, 10))
    main_frame.config(labelanchor='n')
    # main_frame.grid(row=0, column=0, padx=10, pady=10)
    main_frame.pack(padx=10, pady=10)

    bukkit_select_button = ttk.Button(detail_settings_ui, text="적용", width=10, command=define_settings)
    # bukkit_select_button.grid(row=0, column=1, padx=5)
    bukkit_select_button.pack(padx=10, pady=10)

    motd_frame = ttk.LabelFrame(detail_settings_ui, text="MOTD", padding=(20, 10))
    motd_frame.config(labelanchor='n')
    # motd_frame.grid(row=1, column=0, padx=10, pady=10)
    motd_frame.pack(side=tk.LEFT, padx=10, pady=10)

    motd_frame2 = ttk.LabelFrame(detail_settings_ui, text="MOTD", padding=(20, 10))
    motd_frame2.config(labelanchor='n')
    # motd_frame2.grid(row=1, column=1, padx=10, pady=10)
    motd_frame2.pack(side=tk.LEFT, padx=10, pady=10)

    gamemode_label = tk.Label(main_frame, text="게임 모드")
    gamemode_label.grid(row=1, column=0, padx=5, pady=5)

    global gamemode_box
    gamemode_box = ttk.Combobox(main_frame, width=10, values=gamemodes)
    gamemode_box.current(gamemode)
    gamemode_box.grid(row=1, column=1, padx=5, pady=5)

    difficulty_label = tk.Label(main_frame, text="난이도")
    difficulty_label.grid(row=2, column=0, padx=5, pady=5)

    global difficulty_box
    difficulty_box = ttk.Combobox(main_frame, width=10, values=difficulties)
    difficulty_box.current(difficulty)
    difficulty_box.grid(row=2, column=1, padx=5, pady=5)

    level_type_label = tk.Label(main_frame, text="레벨 타입")
    level_type_label.grid(row=3, column=0, padx=5, pady=5)

    global level_type_box
    level_type_box = ttk.Combobox(main_frame, width=10, values=leveltypes)
    level_type_box.current(level_type)
    level_type_box.grid(row=3, column=1, padx=5, pady=5)

    pvp_label = tk.Label(main_frame, text="PvP")
    pvp_label.grid(row=6, column=0, padx=5, pady=5)

    global pvp_box
    pvp_box = ttk.Checkbutton(main_frame, variable=pvpVar)
    pvp_box.grid(row=6, column=1, padx=5, pady=5)

    spawn_protection_label = tk.Label(main_frame, text="스폰 보호")
    spawn_protection_label.grid(row=4, column=0, padx=5, pady=5)

    global spawn_protection_box
    spawn_protection_box = ttk.Spinbox(main_frame, from_=0, to=100, increment=1, width=5)
    spawn_protection_box.delete(0, tk.END)
    spawn_protection_box.insert(0, spawn_protection)
    spawn_protection_box.grid(row=4, column=1, padx=5, pady=5)

    allow_flight_label = tk.Label(main_frame, text="비행 허용")
    allow_flight_label.grid(row=7, column=0, padx=5, pady=5)

    global allow_flight_box
    allow_flight_box = ttk.Checkbutton(main_frame, variable=allowFlightVar)
    allow_flight_box.grid(row=7, column=1, padx=5, pady=5)

    max_players_label = tk.Label(main_frame, text="최대 플레이어 수")
    max_players_label.grid(row=5, column=0, padx=5, pady=5)

    global max_players_box
    max_players_box = ttk.Spinbox(main_frame, from_=0, to=100, increment=1, width=5)
    max_players_box.delete(0, tk.END)
    max_players_box.insert(0, max_players)
    max_players_box.grid(row=5, column=1, padx=5, pady=5)

    allow_command_block_label = tk.Label(main_frame, text="커맨드 블록 허용")
    allow_command_block_label.grid(row=8, column=0, padx=5, pady=5)

    global allow_command_block_box
    allow_command_block_box = ttk.Checkbutton(main_frame, variable=allowCommVar)
    allow_command_block_box.grid(row=8, column=1, padx=5, pady=5)

    port_label = tk.Label(main_frame, text="포트")
    port_label.grid(row=10, column=0, padx=5, pady=5)

    global port_box
    port_box = ttk.Entry(main_frame, width=14)
    port_box.insert(0, port)
    port_box.grid(row=10, column=1, padx=5, pady=5)

    whitelist_label = tk.Label(main_frame, text="화이트리스트")
    whitelist_label.grid(row=9, column=0, padx=5, pady=5)

    global whitelist_box
    whitelist_box = ttk.Checkbutton(main_frame, variable=whitelistVar)
    whitelist_box.grid(row=9, column=1, padx=5, pady=5)

    motd_label = tk.Label(motd_frame, text="MOTD")
    motd_label.grid(row=0, column=0, padx=5, pady=5)

    motd_label = tk.Label(motd_frame, text="MOTD 미리보기")
    motd_label.grid(row=1, column=0, padx=5, pady=5)

    global motd_box
    motd_box = tk.Text(motd_frame, width=20, height=5, wrap=tk.WORD, state='normal')
    motd_box.insert(tk.INSERT, motd)
    motd_box.grid(row=0, column=1, padx=5, pady=5)
    motd_box.bind("<KeyRelease>", motd_change_preview)

    def motd_bold():
        motd_box.insert(tk.INSERT, "§l")
        motd_change_preview(None)

    motd_bold_button = ttk.Button(motd_frame2, text="굵게", width=5, command=motd_bold)
    motd_bold_button.grid(row=3, column=1, padx=5, pady=12)

    def motd_italic():
        motd_box.insert(tk.INSERT, "§o")
        motd_change_preview(None)

    motd_italic_button = ttk.Button(motd_frame2, text="기울임", width=5, command=motd_italic)
    motd_italic_button.grid(row=3, column=2, padx=5, pady=12)

    def motd_underline():
        motd_box.insert(tk.INSERT, "§n")
        motd_change_preview(None)

    motd_underline_button = ttk.Button(motd_frame2, text="밑줄", width=5, command=motd_underline)
    motd_underline_button.grid(row=3, column=3, padx=5, pady=12)

    def motd_strike():
        motd_box.insert(tk.INSERT, "§m")
        motd_change_preview(None)

    motd_strike_button = ttk.Button(motd_frame2, text="취소선", width=5, command=motd_strike)
    motd_strike_button.grid(row=4, column=1, padx=5, pady=12)

    def motd_obfuscated():
        motd_box.insert(tk.INSERT, "§k")
        motd_change_preview(None)

    motd_obfuscated_button = ttk.Button(motd_frame2, text="난독화", width=5, command=motd_obfuscated)
    motd_obfuscated_button.grid(row=4, column=2, padx=5, pady=12)

    global motd_color
    global motd_color_box
    motd_color = ["검정", "짙은 파랑", "짙은 초록", "진한 청록", "진한 빨강", "진한 보라", "금색", "회색", "짙은 회색", "파랑", "초록", "청록", "빨강", "보라", "노랑", "백색"]
    motd_color_box = ttk.Combobox(motd_frame2, width=2, values=motd_color, state="readonly")
    motd_color_box.grid(row=4, column=3, padx=5, pady=12)
    motd_color_box.bind("<<ComboboxSelected>>", motd_color_set)

    def motd_reset():
        motd_box.insert(tk.INSERT, "§r")
        motd_change_preview(None)

    motd_reset_button = ttk.Button(motd_frame2, text="초기화", width=5, command=motd_reset)
    motd_reset_button.grid(row=5, column=2, padx=5, pady=12)

    global motd_preview
    motd_preview = tk.Text(motd_frame, width=20, height=5, wrap=tk.WORD)
    motd_preview.insert(tk.INSERT, motd_P)
    motd_preview.config(state='disabled')
    motd_preview.grid(row=1, column=1, padx=5, pady=5)

def define_settings():
    global gamemode, difficulty, pvp, spawn_protection, allow_flight, max_players, allow_command_block, port, whitelist, motd, level_type
    gamemode = gamemode_box.current()
    difficulty = difficulty_box.current()
    level_type = level_type_box.current()
    pvp = pvpVar.get()
    spawn_protection = int(spawn_protection_box.get())
    allow_flight = allowFlightVar.get()
    max_players = int(max_players_box.get())
    allow_command_block = allowCommVar.get()
    port = int(port_box.get())
    whitelist = whitelistVar.get()
    motd = motd_box.get("1.0", tk.END)

    detail_settings_ui.destroy()

    detail_settings_text.config(text=f"게임모드: {gamemodes[gamemode]}\n난이도: {difficulties[difficulty]}\n레벨 타입: {leveltypes[level_type]}\nPvP: {pvp}\n스폰 보호: {spawn_protection}\n비행 허용: {allow_flight}\n최대 플레이어 수: {max_players}\n커맨드 블록 허용: {allow_command_block}\n포트: {port}\n화이트리스트: {whitelist}\nMOTD: {motd}")

def change_theme() -> None:
    '''테마 변경 클릭 시 호출되는 함수, 현재 테마를 불러오며 테마 변경함.'''
    
    global theme_img
    if sv_ttk.get_theme() == "dark":
        sv_ttk.set_theme("light")
        theme_img = light_mode_img
    else:
        sv_ttk.set_theme("dark")
        theme_img = dark_mode_img

    dark_light_mode_change.config(image=theme_img)

    font_f = ft.nametofont("TkDefaultFont").actual()["family"]
    font = ft.Font(family=ft.nametofont("TkDefaultFont").actual()["family"], size=10)

    style = ttk.Style(window)
    style.configure("TButton", font=font)
    style.configure("TLabelframe", font=font)
    style.configure("TFrame", font=font)
    style.configure("Treeview.Heading", font=font)

    apply_theme_to_titlebar(window)

    config_write("theme", str(sv_ttk.get_theme()).lower())

if __name__ == "__main__":

    original_dir = os.getcwd()
    config_write("version", version)

    window = tk.Tk()
    window.title("")

    window.iconbitmap(default=ICON_PATH)
    window.resizable(False, False)

    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())
    x_cordinate = int((window.winfo_screenwidth() / 2) - (window.winfo_width() / 2))
    y_cordinate = int((window.winfo_screenheight() / 2) - (window.winfo_height() / 2))
    window.geometry("+{}+{}".format(x_cordinate-140, y_cordinate-140))

    window.wm_attributes("-topmost", 1)

    try: sv_ttk.set_theme(config_read("theme"))
    except:
        try:
            sv_ttk.set_theme(darkdetect.theme())
            config_write("theme", str(darkdetect.theme()).lower())
        except:
            sv_ttk.set_theme("dark")
            config_write("theme", "dark")

    font_f = ft.nametofont("TkDefaultFont").actual()["family"]
    font = ft.Font(family=ft.nametofont("TkDefaultFont").actual()["family"], size=10)

    style = ttk.Style(window)
    style.configure("TButton", font=font)
    style.configure("TLabelframe", font=font)
    style.configure("TFrame", font=font)
    style.configure("Treeview.Heading", font=font)

    # tk 변수

    pvpVar = tk.BooleanVar()
    pvpVar.set(True)
    allowCommVar = tk.BooleanVar()
    allowCommVar.set(False)
    whitelistVar = tk.BooleanVar()
    whitelistVar.set(False)
    allowFlightVar = tk.BooleanVar()
    allowFlightVar.set(False)
    p_var = tk.DoubleVar()

    # tk 변수

    main_frame = ttk.LabelFrame(window, text="Make", padding=(20, 10))
    main_frame.config(labelanchor='n')
    main_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    detail_text = tk.Label(window, text=f"버킷 생성기 {version}\nMade by _Richardo")
    detail_text.grid(row=1, column=0, pady=5, columnspan=2)

    etc_frame = ttk.LabelFrame(window, padding=(20, 10))
    etc_frame.config(labelanchor='n')
    etc_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    dark_mode_img = tk.PhotoImage(file=resource_path("resources/dark_mode.png")).subsample(20)
    light_mode_img = tk.PhotoImage(file=resource_path("resources/light_mode.png")).subsample(20)

    update_button_img = tk.PhotoImage(file=resource_path("resources/updates.png")).subsample(20)
    if config_read("theme") == "dark": theme_img = dark_mode_img
    else: theme_img = light_mode_img
    dark_light_mode_change = ttk.Button(etc_frame, image=theme_img, command=change_theme)
    dark_light_mode_change.grid(row=0, column=0, pady=5, padx=5)

    update_button = ttk.Button(etc_frame, image=update_button_img, command=get_updates)
    update_button.grid(row=0, column=1, pady=5, padx=5)

    settings_frame = ttk.LabelFrame(window, text="Settings", padding=(20, 10))
    settings_frame.config(labelanchor='n')
    settings_frame.grid(row=3, column=0, padx=10, pady=10)

    bukkit_frame = ttk.LabelFrame(window, text="Bukkit", padding=(20, 10))
    bukkit_frame.config(labelanchor='n')
    bukkit_frame.grid(row=3, column=1, padx=10, pady=10)

    dir_label = tk.Label(main_frame, text="경로")
    dir_label.grid(row=0, column=0, padx=5, pady=5)

    dir_path = ttk.Entry(main_frame, width=25, font=font)
    try: config_read('dir')
    except KeyError: config_write('dir', "")
    dir_path.insert(0, config_read('dir'))
    dir_path.config(state='readonly')
    dir_path.grid(row=0, column=1, padx=5, pady=5)

    open_dir_button = ttk.Button(main_frame, text="열기", width=5, command=open_dir)
    open_dir_button.grid(row=0, column=2, padx=5, pady=5)
    dir_path.grid(row=0, column=1, padx=5, pady=5)

    folder_name = tk.Label(main_frame, text="폴더 이름")
    folder_name.grid(row=2, column=0, padx=5, pady=5)

    folder_name_entry = ttk.Entry(main_frame, width=25, font=font)
    folder_name_entry.grid(row=2, column=1, padx=5, pady=5)

    try: config_read('name')
    except KeyError: config_write('name', "{번호}. {버전}_{버킷}_버킷")
    folder_name_entry.insert(0, config_read('name'))

    folder_name_save = ttk.Button(main_frame, text="저장", width=5, command=folder_name_savef)
    folder_name_save.grid(row=2, column=2, padx=5, pady=5)

    folder_name_reset = ttk.Button(main_frame, text="초기화", width=5, command=folder_name_resetf)
    folder_name_reset.grid(row=2, column=3, padx=5, pady=5)

    min_ram_label = tk.Label(settings_frame, text="최소 램")
    min_ram_label.grid(row=0, column=0, padx=5, pady=5)

    ram_box_values = [f'{i}G' for i in range(1, 13)]

    min_ram_box = ttk.Combobox(settings_frame, width=3, values=ram_box_values, state='readonly')
    min_ram_box.current(3)
    min_ram_box.grid(row=0, column=1, padx=5, pady=5)

    max_ram_label = tk.Label(settings_frame, text="최대 램")
    max_ram_label.grid(row=1, column=0, padx=5, pady=5)

    max_ram_box = ttk.Combobox(settings_frame, width=3, values=ram_box_values, state='readonly')
    max_ram_box.current(3)
    max_ram_box.grid(row=1, column=1, padx=5, pady=5)

    bukkit_status_label = tk.Label(bukkit_frame, text="버킷 종류")
    bukkit_status_label.grid(row=0, column=0, padx=5, pady=5)

    bukkit_genre = ttk.Entry(bukkit_frame, width=10, font=font)
    bukkit_genre.grid(row=0, column=1, padx=5, pady=5)
    bukkit_genre.config(state='readonly')

    bukkit_version_label = tk.Label(bukkit_frame, text="버전")
    bukkit_version_label.grid(row=1, column=0, padx=5, pady=5)

    bukkit_version = ttk.Entry(bukkit_frame, width=10, font=font)
    bukkit_version.grid(row=1, column=1, padx=5, pady=5)
    bukkit_version.config(state='readonly')

    bukkit_build_label = tk.Label(bukkit_frame, text="빌드")
    bukkit_build_label.grid(row=2, column=0, padx=5, pady=5)

    bukkit_build_v = ttk.Entry(bukkit_frame, width=10, font=font)
    bukkit_build_v.grid(row=2, column=1, padx=5, pady=5)
    bukkit_build_v.config(state='readonly')

    get_bukkit = ttk.Button(bukkit_frame, text="버킷 선택", width=10, command=get_bukkit_info, state=tk.DISABLED)
    if config_read('dir') != "": get_bukkit.config(state=tk.NORMAL)
    get_bukkit.grid(row=3, column=1, pady=5)

    java_dir_label = tk.Label(main_frame, text="자바 경로")
    java_dir_label.grid(row=1, column=0, padx=5, pady=5)

    java_dir_path = ttk.Entry(main_frame, width=25, font=font)
    java_dir_path.insert(0, "(자동 탐지)")
    java_dir_path.config(state='readonly')
    java_dir_path.grid(row=1, column=1, padx=5, pady=5)

    open_dir_button2 = ttk.Button(main_frame, text="열기", width=5, command=open_dir2)
    open_dir_button2.grid(row=1, column=2, padx=5, pady=5)

    clear_dir_button2 = ttk.Button(main_frame, text="초기화", width=5, command=clear_dir)
    clear_dir_button2.grid(row=1, column=3, padx=0, pady=5)

    etc_server_settings_button = ttk.Button(settings_frame, text="서버 설정", width=10, command=etc_settings, state=tk.DISABLED)
    etc_server_settings_button.grid(row=3, column=0, pady=5)

    plugins_button = ttk.Button(settings_frame, text="플러그인", width=7, command=open_plugin_list, state=tk.DISABLED)
    plugins_button.grid(row=3, column=1, pady=5)

    mods_button = ttk.Button(settings_frame, text="모드", width=7, command=open_mods_list, state=tk.DISABLED)
    mods_button.grid(row=4, column=1, pady=8)

    create_button = ttk.Button(main_frame, text="버킷 제작", width=10, command=create_thread, state=tk.DISABLED)
    create_button.grid(row=3, column=1, pady=5)

    progress_bar = ttk.Progressbar(main_frame, length=200, maximum=100, variable=p_var)
    progress_bar.grid(row=4, column=1, padx=5, pady=5)

    progress_text = tk.Label(main_frame, text="대기 중")
    progress_text.grid(row=5, column=1, padx=5, pady=5)

    apply_theme_to_titlebar(window)

    if not os.path.exists("updater.exe"):
        # messagebox.showerror("Error", "자동 업데이터 파일이 없어 자동으로 다운로드합니다.")
        show_error("오류", "자동 업데이터 파일이 없어 자동으로 다운로드합니다.")
        download("https://www.richardo.net/files/bukkits/updater.exe", ".", "updater.exe")

    if check_update(version):
        get_updates()

    window.mainloop()