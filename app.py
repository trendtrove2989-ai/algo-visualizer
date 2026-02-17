from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/run-visualizer')
def run_app():
    # This command launches your Nexus Grid [cite: 54]
    subprocess.Popen(['python', 'main.py'])
    return "Visualizer Started!"

if __name__ == '__main__':
    app.run(port=5000)