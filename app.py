from flask import Flask, send_file, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_music', methods=['POST'])
def generate_music():
    # Run your scripts in the correct order
    subprocess.run(['python', 'preprocess.py'])
    subprocess.run(['python', 'train_model.py'])
    subprocess.run(['python', 'generate_music.py'])
    subprocess.run(['python', 'save_music.py'])
    
    # Replace this with the actual generated notes from your script
    generated_notes = ['C4', 'D4', 'E4', 'F4', 'G4']  # Example generated notes

    return jsonify(generated_notes), 200

@app.route('/download')
def download_file():
    return send_file('generated_music.mid', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
