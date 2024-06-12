from flask import Flask, request, jsonify, render_template, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the video file
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    # Convert video to MP3
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(file.filename)[0] + '.mp3')
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    # Return the MP3 file as a download response
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
