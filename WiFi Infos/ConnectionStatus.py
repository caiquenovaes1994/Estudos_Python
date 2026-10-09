import subprocess

status = subprocess.check_output(
    'netsh wlan show interfaces',
    shell=True
).decode()

print(status)