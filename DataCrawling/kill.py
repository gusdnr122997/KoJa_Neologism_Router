import psutil

for p in psutil.process_iter():
    if p.name() == 'chrome.exe' or p.name() == 'chromedriver.exe':
        p.kill()