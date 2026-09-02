from flask import Flask, render_template
import subprocess

app = Flask(__name__)

scripts = {
    "helloworld" : "/home/axlrose/projects/server/scripts/hello-world.sh" 
    ,"err_test":"/home/axlrose/projects/server/scripts/err.sh"
}

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
    app.run(host = '0.0.0.0', port=5000, debug=True)
