from flask import Flask, render_template
from datetime import datetime, timezone
import subprocess
import json

app = Flask(__name__)

scripts = {
    "helloworld" : "/home/axlrose/projects/server/scripts/hello-world.sh" 
    ,"err_test":"/home/axlrose/projects/server/scripts/err.sh"
}

def docker_list_container():
    docker_list = {}
    result = subprocess.run(["docker","ps","-q"], capture_output = True, text = True)
    for index, val in enumerate(result.stdout.splitlines()):
        docker_list[index] = val
    return docker_list

containers = []

def container_getinfo(docker_list):
    container_info = {}
    for index in docker_list.values():
        if not index:
            continue

        result = subprocess.run(["docker","inspect",index], capture_output = True, text = True) 
        data = json.loads(result.stdout)[0]
    
        name = data["Name"].lstrip("/")
        state = data["State"]["Status"]
        started = data["State"]["StartedAt"]

        started_time = datetime.fromisoformat(
            started.replace("Z", "+00:00")
        )

        uptime = datetime.now(timezone.utc) - started_time

        container_info["name"] = name
        container_info["state"] = state
        container_info["uptime"] = uptime
        container_info["last_restart"] = started        

        containers.append(container_info)

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/run_helloworld', methods = ['GET'])
def run_helloworld():
    result = subprocess.run(["bash",scripts["err_test"]], 
                   capture_output = True,
                   text = True) 

    output = result.stdout + result.stderr
    ret_code = result.returncode
    return render_template('result.html', 
                           output=output,
                           returncode = ret_code)

if __name__ == '__main__':
    docker_list = docker_list_container()
    container_getinfo(docker_list)
    app.run(host = '0.0.0.0', port=5000, debug=True)
