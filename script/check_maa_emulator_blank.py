import os

import yaml
from requests import get
import win32gui
import win32process
import psutil
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

pwd = Path(__file__).parent

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename=pwd.joinpath("check_maa_emulator.log").as_posix(),
                                   when="D", backupCount=1, encoding="utf-8", utc=False)

formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

handler.setFormatter(formatter)
logger.addHandler(handler)

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

with open(pwd.joinpath('check_maa.yaml').as_posix(), encoding='utf-8') as fn:
    content = yaml.load(fn, Loader=yaml.FullLoader)

resp = get('')
config = resp.json()
bot_token = config['bot_token']


def running(exe):
    status = any(p.info["exe"] and p.info["exe"].lower() == exe.lower() for p in psutil.process_iter(["exe"]))
    return status


def status(s):
    return 'On' if s else 'Off'


for n, details in content.items():
    e = details['exe_location']
    t = details['emulator_name']
    i = details['chat_id']

    # MAA
    status1 = running(e)
    print(n, 'MAA', status1)

    logger.info(f'{n} MAA status: {status(status1)}')

    if not status1:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={i}&text=MAA not running for {n}"
        try:
            get(url)
            logger.info(f'{n} MAA notification: sent')
        except:
            logger.info(f'{n} MAA notification: failed')

    # Emulator
    status2 = False
    for hwnd, pid, title in results:
        if title == t:
            status2 = True
            break

    print(n, 'Emulator', status2)
    logger.info(f'{n} Emulator status: {status(status2)}')

    if not status2:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={i}&text=Emulator not running for {n}"
        try:
            get(url)
            logger.info(f'{n} Emulator notification: sent')
        except:
            logger.info(f'{n} Emulator notification: failed')
