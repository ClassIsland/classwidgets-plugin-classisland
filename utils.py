import os
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import requests

def get_classisland_path():
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, "ClassIsland")

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    with open(dest_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def download_and_extract_classisland():
    url = "https://get.classisland.tech/d/ClassIsland-Ningbo-S3/classisland/disturb/1.5.3.1/ClassIsland_app_windows_x64_full_singleFile.zip"
    classisland_path = get_classisland_path()
    dest_path = os.path.join(classisland_path, "ClassIsland_app_windows_x64_full_singleFile.zip")
    
    # 检查并创建目录
    if not os.path.exists(classisland_path):
        os.makedirs(classisland_path)
    
    # 使用多线程下载文件
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(download_file, url, dest_path)
        future.result()  # 等待下载完成

    # 解压文件
    with ZipFile(dest_path, 'r') as zip_ref:
        zip_ref.extractall(classisland_path)

    # 删除下载的zip文件
    os.remove(dest_path)
    return os.path.join(classisland_path,"ClassIsland.exe")