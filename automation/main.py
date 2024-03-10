import requests
import pathlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os, sys
urllib3.disable_warnings(InsecureRequestWarning)
import json
import bs4
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
    if (pathlib.Path(__file__).parents[1] /  "manifests" / id[0].lower() / id.replace(".", "/") / version).exists():
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
                w.write(json.dumps(JSON, indent=2, sort_keys=True))
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

# Add HandBrake.HandBrake_Pckgr to Update List
    id = "HandBrake.HandBrake_Pckgr"
    JSON = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("blockmap" in each["browser_download_url"]) or ("sig" in each["browser_download_url"])) and (("arm64" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

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

# Add WinMerge.WinMerge_Pckgr to Update List
    id = "WinMerge.WinMerge_Pckgr"
    JSON = requests.get("https://api.github.com/repos/WinMerge/winmerge/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/WinMerge/winmerge/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add dbeaver.dbeaver_Pckgr to Update List
    id = "dbeaver.dbeaver_Pckgr"
    JSON = requests.get("https://api.github.com/repos/dbeaver/dbeaver/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dbeaver/dbeaver/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add GitHub.cli_Pckgr to Update List
    id = "GitHub.cli_Pckgr"
    JSON = requests.get("https://api.github.com/repos/cli/cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/cli/cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi") and not("386" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Greenshot.Greenshot_Pckgr to Update List
    id = "Greenshot.Greenshot_Pckgr"
    JSON = requests.get("https://api.github.com/repos/greenshot/greenshot/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/greenshot/greenshot/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("PortableApps" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add JGraph.Draw_Pckgr to Update List
    id = "JGraph.Draw_Pckgr"
    JSON = requests.get("https://api.github.com/repos/jgraph/drawio-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jgraph/drawio-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not(("no" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.AzureCLI_Pckgr to Update List
    id = "Microsoft.AzureCLI_Pckgr"
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/Azure/azure-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [
    f"https://azcliprod.azureedge.net/msi/azure-cli-{Version}.msi",
    f"https://azcliprod.azureedge.net/msi/azure-cli-{Version}-x64.msi"]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add Microsoft.Bicep_Pckgr to Update List
    id = "Microsoft.Bicep_Pckgr"
    JSON = requests.get("https://api.github.com/repos/Azure/bicep/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Azure/bicep/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and ("setup" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.BotFrameworkComposer_Pckgr to Update List
    id = "Microsoft.BotFrameworkComposer_Pckgr"
    JSON = requests.get("https://api.github.com/repos/microsoft/BotFramework-Composer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/BotFramework-Composer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.BotFrameworkEmulator_Pckgr to Update List
    id = "Microsoft.BotFrameworkEmulator_Pckgr"
    JSON = requests.get("https://api.github.com/repos/microsoft/BotFramework-Emulator/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/BotFramework-Emulator/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.PowerToys_Pckgr to Update List
    id = "Microsoft.PowerToys_Pckgr"
    JSON = requests.get("https://api.github.com/repos/microsoft/PowerToys/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/PowerToys/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.WindowsTerminal to Update List
    id = "Microsoft.WindowsTerminal"
    JSON = requests.get("https://api.github.com/repos/microsoft/terminal/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/terminal/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msixbundle")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.XMLNotepad_Pckgr to Update List
    id = "Microsoft.XMLNotepad_Pckgr"
    JSON = requests.get("https://api.github.com/repos/microsoft/XmlNotepad/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/XmlNotepad/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msixbundle")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Notepad++.Notepad++_Pckgr to Update List
    id = "Notepad++.Notepad++_Pckgr"
    JSON = requests.get("https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("sig" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), str_pop(Version, 0), id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add OpenJS.NodeJS_Pckgr to Update List
    id = "OpenJS.NodeJS_Pckgr"
    Urls:list[str] = [each["href"] for each in bs4.BeautifulSoup(requests.get("https://nodejs.org/dist/latest/", verify=False).text, "html.parser").pre.find_all("a") if "msi" in each["href"]]
    Version = clean_string(Urls[0], {"node-v":"", "-":"", ".msi":"", "arm64":"", "x64":"", "x86":""})
    Urls = ["https://nodejs.org/dist/{}/{}".format("v"+Version ,each) for each in Urls]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

    # Check for missing versions
    try:
        for each in requests.get("https://nodejs.org/dist/index.json").json():
            if not each["lts"]:
                continue
            id = "OpenJS.NodeJS.LTS_Pckgr"
            JSON = each["files"]
            Version = each["version"]
            _ = {"win-": f"node-v{Version}-", "-msi": ".msi"}
            Urls = [f"https://nodejs.org/dist/{Version}/{clean_string(each, _)}" for each in JSON if "-msi" in each]
            if not version_verify(Version, id):
                report_existed(id, Version)
            elif do_list(id, Version, "verify"):
                report_existed(id, Version)
            else:
                Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
            del Urls, Version, id
            
    except BaseException as e:
        print("Got error while checking: ", e)
        
    # Updating
    if not debug:
        for each in Commands:
            if os.system(each[0]) == 0:
                do_list(*each[1])

    return Commands

if __name__ == "__main__":
    print([each[0] for each in main()])
