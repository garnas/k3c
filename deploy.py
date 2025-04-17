import os
import shutil

import paramiko
from dotenv import dotenv_values
from scp import SCPClient
import subprocess

config = dotenv_values(".env")
hostname = config["hostname"]
username = config["username"]
password = config["password"]
port = int(config["port"])
frontend_dir = os.path.join("frontend")
dist_source = os.path.join(frontend_dir, "dist")
dist_target = "/home/myapp/frontend"
cert_source = os.path.join(".cert")
cert_target = "/home/myapp/.cert"

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

commands_build = f"""
cd /home/myapp
rm -rf {dist_target}
rm -rf {cert_target}
git fetch origin master
git diff origin/master
git reset --hard origin/master
git clean -fd
"""

commands_gunicorn = """
cd /home/myapp
. .venv/bin/activate
pkill gunicorn
gunicorn --certfile=.cert/cer.cer --keyfile=.cert/key.key -w 2 -b 0.0.0.0:443 'backend.app:app' --daemon
"""

try:
    ssh.connect(hostname, port, username, password)
    _, stdout, stderr = ssh.exec_command(commands_build)
    print(stdout.read().decode())
    print(stderr.read().decode())
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(dist_source, dist_target, recursive=True)
        scp.put(cert_source, cert_target, recursive=True)

    _, stdout, stderr = ssh.exec_command(commands_gunicorn)
    print(stdout.read().decode())
    print(stderr.read().decode())
finally:
    # Close the connection
    ssh.close()
