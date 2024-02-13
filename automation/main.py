import requests
import pathlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os, sys
urllib3.disable_warnings(InsecureRequestWarning)
import json
import re

GH_TOKEN = os.environ["GITHUB_TOKEN"]

def report_existed(id: str, Version: str) -> None:
    print(f"{id}: {Version} has already existed, skip publishing")

def wingetcreate(path: str, debug: bool = False) -> str:
    return "wingetcreate"

def command(wingetcreate: pathlib.Path, urls: str, version: str,  id: str, token: str) -> str:
    Commands = "{} update --submit --urls {} --version {} {} --token {}".format(wingetcreate.__str__(), urls, version, id, token)
    return Commands

def clean_string(string: str, keywords: dict[str, str]) -> str:
    for k in keywords:
        string = string.replace(k, keywords[k])
    return string

def str_pop(string: str, index: int) -> str:
        i = list(string)
        i.pop(index)
        i = "".join(i)

        return i

def list_to_str(List: list) -> str:
    new = str(List)
    new = clean_string(new, {
         "[": "",
         "]": "",
         " ": "",
         "'": "",
         ",": " "
    })
    return new

def version_verify(version: str, id: str) -> bool:
    pkg_path = "manifests" / id[0].lower() / id.replace(".", "/")
    if (pathlib.Path(__file__).parents[1] / pkg_path / version).exists():
        return False
    else:
        return True

def do_list(id: str, version: str, mode: str) -> bool | None:
    """
    Mode: write or verify
    """
    path = pathlib.Path(__file__).parents[0] / "list.json"
    with open(path, "r", encoding="utf-8") as f:
        try:
            JSON: dict[str, list[str]] = json.loads(f.read())
        except BaseException:
            JSON: dict[str, list[str]] = {}
        if id not in JSON:
            JSON[id] = []
        
        if mode == "write":
            if version not in JSON[id]:
                JSON[id].append(version)
            with open(path, "w+", encoding="utf-8") as w:
                w.write(json.dumps(JSON))
        elif mode == "verify":
            if version in JSON[id]:
                return True
            else:
                return False
        else:
            raise Exception
 
def main() -> list[tuple[str, tuple[str, str, str]]]:
    Commands:list[tuple[str, tuple[str, str, str]]] = []
    debug = bool([each for each in sys.argv if each == "debug"])
    Wingetcreate = wingetcreate(pathlib.Path(__file__).parents[0], debug)
    Headers = [{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Authorization": f"Bearer {GH_TOKEN}"
    }]

# Add GitHub.Atom_Pckgr to Update List
    id = "GitHub.Atom_Pckgr"
    JSON = requests.get("https://api.github.com/repos/atom/atom/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/atom/atom/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and ("x64" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add GitHub.GitLFS_Pckgr to Update List
    id = "GitHub.GitLFS_Pckgr"
    JSON = requests.get("https://api.github.com/repos/git-lfs/git-lfs/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/git-lfs/git-lfs/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Rufus.Rufus_Pckgr to Update List
    id = "Rufus.Rufus_Pckgr"
    JSON = requests.get("https://api.github.com/repos/pbatard/rufus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/pbatard/rufus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kopia.KopiaUI_Pckgr to Update List
    id = "Kopia.KopiaUI_Pckgr"
    JSON = requests.get("https://api.github.com/repos/kopia/kopia/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kopia/kopia/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kitware.CMake_Pckgr to Update List
    id = "Kitware.CMake_Pckgr"
    JSON = requests.get("https://api.github.com/repos/Kitware/CMake/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Kitware/CMake/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add dnGrep.dnGrep_Pckgr to Update List
    id = "dnGrep.dnGrep_Pckgr"
    JSON = requests.get("https://api.github.com/repos/dnGrep/dnGrep/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dnGrep/dnGrep/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Audacity.Audacity_Pckgr to Update List
    id = "Audacity.Audacity_Pckgr"
    JSON = requests.get("https://api.github.com/repos/audacity/audacity/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/audacity/audacity/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Sonosaurus.SonoBus_Pckgr to Update List
    id = "Sonosaurus.SonoBus_Pckgr"
    JSON = requests.get("https://api.github.com/repos/sonosaurus/sonobus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/sonosaurus/sonobus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kubernetes.minikube_Pckgr to Update List
    id = "Kubernetes.minikube_Pckgr"
    JSON = requests.get("https://api.github.com/repos/kubernetes/minikube/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kubernetes/minikube/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add AutoHotkey.AutoHotkey_Pckgr to Update List
    id = "AutoHotkey.AutoHotkey_Pckgr"
    JSON = requests.get("https://api.github.com/repos/AutoHotkey/AutoHotkey/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AutoHotkey/AutoHotkey/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add JohnMacFarlane.Pandoc_Pckgr to Update List
    id = "JohnMacFarlane.Pandoc_Pckgr"
    JSON = requests.get("https://api.github.com/repos/jgm/pandoc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jgm/pandoc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add DuongDieuPhap.ImageGlass_Pckgr to Update List
    id = "DuongDieuPhap.ImageGlass_Pckgr"
    JSON = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Nextcloud.NextcloudDesktop_Pckgr to Update List
    id = "Nextcloud.NextcloudDesktop_Pckgr"
    JSON = requests.get("https://api.github.com/repos/nextcloud-releases/desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nextcloud-releases/desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add KeePassXCTeam.KeePassXC_Pckgr to Update List
    id = "KeePassXCTeam.KeePassXC_Pckgr"
    JSON = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("msi" in each["browser_download_url"]) and not("sig" in each["browser_download_url"]) or (("-LegacyWindows.msi" in each["browser_download_url"]) or ("DIGEST" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.Azure.StorageExplorer_Pckgr to Update List
    id = "Microsoft.Azure.StorageExplorer_Pckgr"
    JSON = requests.get("https://api.github.com/repos/microsoft/AzureStorageExplorer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/AzureStorageExplorer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add RedHat.Podman-Desktop_Pckgr to Update List
    id = "RedHat.Podman-Desktop_Pckgr"
    JSON = requests.get("https://api.github.com/repos/containers/podman-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/containers/podman-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("setup.exe") and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add dotPDNLLC.paintdotnet_Pckgr to Update List
    id = "dotPDNLLC.paintdotnet_Pckgr"
    JSON = requests.get("https://api.github.com/repos/paintdotnet/release/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/paintdotnet/release/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip") and not(("winmsi" in each["browser_download_url"]) or ("portable" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Updating
    if not debug:
        for each in Commands:
            if os.system(each[0]) == 0:
                do_list(*each[1])

    return Commands

if __name__ == "__main__":
    print([each[0] for each in main()])
