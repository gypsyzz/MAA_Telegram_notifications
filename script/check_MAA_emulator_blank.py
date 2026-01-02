import psutil
from requests import get
import win32gui
import win32process
import psutil
from pathlib import Path
import sys
import yaml

TARGET_PROCESS = "MuMuNxDevice.exe"  # change this

results = []


def enum_windows(hwnd, _):
    if not win32gui.IsWindowVisible(hwnd):
        return

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        proc = psutil.Process(pid)
        if proc.name().lower() == TARGET_PROCESS.lower():
            title = win32gui.GetWindowText(hwnd)
            if title:  # skip empty titles
                results.append((hwnd, pid, title))
    except psutil.NoSuchProcess:
        pass


win32gui.EnumWindows(enum_windows, None)

# for multi-user
# exe_ = ["name", r"file_location", "window_title", "TG_chat_id"]

# # for single user
with open(Path(sys.argv[0]).parent.joinpath('conf', 'chat.yaml')) as f:
    content = yaml.safe_load(f)

bot_token = content['bot_token']
chat_id = content['chat_id']
exe_ = ["name", r"file_location", "window_title", chat_id]

def running(exe):
    status = any(p.info["exe"] and p.info["exe"].lower() == exe.lower() for p in psutil.process_iter(["exe"]))
    return status


for n, e, t, i in [exe_]:
    status1 = running(e)
    print(n, 'MAA', status1)

    if not status1:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={i}&text=MAA not running for {n}"
        get(url)

    status2 = False
    for hwnd, pid, title in results:
        if title == t:
            status2 = True
            break

    print(n, 'Emulator', status2)

    if not status2:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={i}&text=Emulator not running for {n}"
        get(url)
