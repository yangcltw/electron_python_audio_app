from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    transcription = process_audio(filepath)
    return jsonify({"transcription": transcription})

def process_audio(filepath):
    try:
        result = subprocess.run(["whisper", filepath, "--model", "base"], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error: {result.stderr}"

        # 清理轉錄輸出，移除語言檢測訊息與多餘符號
        transcription = result.stdout.strip()
        lines = transcription.splitlines()
        clean_lines = [
            line for line in lines 
            if not line.startswith("Detecting language") and not line.startswith("Detected language")
        ]
        pure_text = "\n".join(clean_lines).strip()
        print(f"output from backend:{pure_text}")
        return pure_text
    
    except Exception as e:
        return f"Error processing audio: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
