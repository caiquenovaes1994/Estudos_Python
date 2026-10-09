import subprocess

result = subprocess.check_output(
    'netsh wlan show interfaces',
    shell=True
).decode()

for line in result.split("\n"):
    if "SSID" in line and "BSSID" not in line:
        print(line)