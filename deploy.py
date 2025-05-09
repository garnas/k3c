import os
import shutil

import paramiko
from dotenv import dotenv_values
from scp import SCPClient
import subprocess

config = dotenv_values(".env")
hostname = config["server.hostname"]
username = config["server.username"]
password = config["server.password"]
port = int(config["server.port"])

frontend_dir = os.path.join("frontend")
dist_source = os.path.join(frontend_dir, "dist")
dist_target = "/home/k3c/frontend"

cert_source = os.path.join(".cer")
cert_target = "/home/k3c/.cer"

dotenv_source = os.path.join(".env-prod")
dotenv_target = "/home/k3c/.env"

git_source = config["git.source"]

commands_build = f"""
cd ../home
rm -rf k3c
git clone {git_source}
cd k3c
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
"""

commands_gunicorn = """
cd ../home/k3c
echo "Activate .venv"
. .venv/bin/activate
echo "Kill gunicorn"
pkill gunicorn
echo "(Re)start gunicorn"
gunicorn --certfile=.cer/cer.cer --keyfile=.cer/key.key -w 1 -b 0.0.0.0:443 --log-level Info --log-file gunicorn.log --max-requests 10000 -k gevent 'backend.app:app' --daemon
"""

if os.path.exists(dist_source):
    print(f"Removing {dist_source} ...")
    shutil.rmtree(dist_source)
result = subprocess.run(
    ["npm", "run", "build"], cwd=os.path.abspath(frontend_dir), shell=True
)
if not os.path.exists(dist_source):
    raise Exception("Failed to build dist directory")

print("Create SSH client instance ...")
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port, username, password)
    _, stdout, stderr = ssh.exec_command(commands_build)
    print(stdout.read().decode())
    print(stderr.read().decode())
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(cert_source, cert_target, recursive=True)
        scp.put(dist_source, dist_target, recursive=True)
        scp.put(dotenv_source, dotenv_target, recursive=True)

    _, stdout, stderr = ssh.exec_command(commands_gunicorn)
    print(stdout.read().decode())
    print(stderr.read().decode())
finally:
    # Close the connection
    ssh.close()
