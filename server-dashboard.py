from flask import Flask, render_template
from datetime import datetime, timezone
import subprocess
import json

app = Flask(__name__)

scripts = {
    "sys-info": "/home/maintainer/server-dashboard/scripts/sys-info.sh",
    "sys-update": "/home/maintainer/server-dashboard/scripts/sys-update.sh",
    "disk-health":"/home/maintainer/server-dashboard/scripts/disk-health.sh",
    "immich-bak": "/home/maintainer/server-dashboard/scripts/immich-bak.sh"
}

def docker_list_container():
    docker_list = {}
    result = subprocess.run(["docker","ps","-aq"], capture_output = True, text = True)
    for index, val in enumerate(result.stdout.splitlines()):
        docker_list[index] = val
    return docker_list

def container_getinfo(docker_list,containers):
    for index in docker_list.values():
        if not index:
            continue
        
        container_info = {} 

        result = subprocess.run(["docker","inspect",index], capture_output = True, text = True) 
        data = json.loads(result.stdout)[0]
    
        name = data["Name"].lstrip("/")
        state = data["State"]["Status"]
        started = data["State"]["StartedAt"]

        started_time = datetime.fromisoformat(
            started.replace("Z", "+00:00")
        )

        last_restart = started_time.strftime("%d-%m-%Y %H:%M:%S")

        uptime = datetime.now(timezone.utc) - started_time
        restarts = data["RestartCount"]
        health = data["State"].get("Health", {}).get("Status", "no healthcheck")

        ports = []
        for port in data["NetworkSettings"]["Ports"].values():
            if port:
                ports.append(port[0]["HostPort"])
        ports = ", ".join(ports)

        container_info["name"] = name
        container_info["state"] = state
        container_info["uptime"] = uptime
        container_info["last_restart"] = last_restart        
        container_info["restarts"] = restarts        
        container_info["health"] = health        
        container_info["ports"] = ports        

        containers.append(container_info)

@app.route('/', methods = ['GET'])
def home():
    containers = []
    docker_list = docker_list_container()
    container_getinfo(docker_list,containers)

    return render_template('dashboard.html', containers = containers)

@app.route('/run_helloworld', methods = ['GET'])
def run_helloworld():
    result = subprocess.run(["bash",scripts["helloworld"]], 
                   capture_output = True, text = True) 

    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html', 
                           output=output, returncode = ret_code)

@app.route('/sys-info', methods = ['GET'])
def system_info():
    result = subprocess.run(["bash",scripts["sys-info"]],
                            capture_output = True, text = True)
    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html',
                           output=output, returncode = ret_code)

@app.route('/sys-update', methods = ['GET'])
def system_update():
    result = subprocess.run(["sudo",scripts["sys-update"]],
                            capture_output = True, text = True)
    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html',
                           output=output, returncode = ret_code)

@app.route('/disk-health', methods = ['GET'])
def disk_health():
    result = subprocess.run(["sudo",scripts["disk-health"]],
                            capture_output = True, text = True)
    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html',
                           output=output, returncode = ret_code)

@app.route('/immich-bak', methods = ['GET'])
def immich_bak():
    result = subprocess.run(["sudo",scripts["immich-bak"]],
                            capture_output = True, text = True)
    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html',
                           output=output, returncode = ret_code)


if __name__ == '__main__': 
    app.run(host = '0.0.0.0', port=5000, debug=True)
