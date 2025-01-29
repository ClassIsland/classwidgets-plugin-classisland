import os
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import requests
import platform
from typing import Tuple, Optional
import hashlib
import sys


def get_classisland_path():
    system = platform.system()
    home_dir = os.path.expanduser("~")
    
    if system == "Windows":
        if os.path.exists("D:"):
            return "D:\\ClassIsland"
        else:
            return os.path.join(home_dir, "Documents", "ClassIsland")
    else:
        documents_path = os.path.join(home_dir, "Documents")
        if os.path.exists(documents_path):
            return os.path.join(documents_path, "ClassIsland")
        else:
            return os.path.join(home_dir, "ClassIsland")


def get_latest_beta_version_info_url() -> Optional[str]:
    url = "https://get.classisland.tech/d/ClassIsland-Ningbo-S3/classisland/disturb/index.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching version info: {e}")
        return None

    latest_beta_version_info_url = None
    for version in data.get("Versions", []):
        if "beta" in version.get("Channels", []):
            if latest_beta_version_info_url is None or version["Version"] > latest_beta_version_info_url["Version"]:
                latest_beta_version_info_url = version

    return latest_beta_version_info_url["VersionInfoUrl"] if latest_beta_version_info_url else None

def get_download_info(version_info_url: str) -> Tuple[Optional[str], Optional[str]]:
    response = requests.get(version_info_url)
    response.raise_for_status()
    data = response.json()

    download_info = data["DownloadInfos"].get("windows_x64_full_singleFile")
    if not download_info:
        return None, None

    download_urls = download_info["ArchiveDownloadUrls"]
    download_url = download_urls.get("main") or download_urls.get("github-origin")
    sha256 = download_info["ArchiveSHA256"]

    return download_url, sha256


def verify_file_sha256(file_path, correct_sha256):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest().upper() == correct_sha256.upper()

def download_file(url, dest_path, progress_callback):
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:  # no content length header
        with open(dest_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    else:
        total_length = int(total_length)
        downloaded = 0
        with open(dest_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    progress = int(100 * downloaded / total_length)
                    progress_callback.emit(progress)

def download_and_extract_classisland(progress_callback):
    version_info_url = get_latest_beta_version_info_url()
    download_info = get_download_info(version_info_url)
    
    
    url = download_info[0]
    file_hash = download_info[1]
    
    classisland_path = get_classisland_path()
    dest_path = os.path.join(classisland_path, "ClassIsland_app_windows_x64_full_singleFile.zip")
    
    # 检查并创建目录
    if not os.path.exists(classisland_path):
        os.makedirs(classisland_path)
    
    # 使用多线程下载文件
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(download_file, url, dest_path, progress_callback)
        future.result()  # 等待下载完成
        
    # 验证文件
    if not verify_file_sha256(dest_path, file_hash):
        print("Downloaded file is corrupted. Aborting.")
        sys.exit(1)

    # 解压文件
    with ZipFile(dest_path, 'r') as zip_ref:
        zip_ref.extractall(classisland_path)

    # 删除下载的zip文件
    os.remove(dest_path)
    return os.path.join(classisland_path, "ClassIsland.exe")