from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from img import process_image  # using img.py
from vid import process_video  # using vid.py

app = Flask(__name__)

# Path set up
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/process_image', methods=['POST'])
def process_image_route():
    image_filename = request.form.get('index')  # Get image filename from the frontend
    image_path = os.path.join(STATIC_FOLDER, 'images', image_filename)
    
    result = process_image('https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop')  # Process the image using your CV logic
    return jsonify({'status': 'success', 'result': result})

@app.route('/process_video', methods=['POST'])
def process_video_route():
    video_filename = request.form.get('index')  # Get video filename
    video_path = os.path.join(STATIC_FOLDER, 'videos', video_filename)

    result = process_video('https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop')  # Process the video using your CV logic
    return jsonify({'status': 'success', 'result': result})

# Serve image or video files from the static folder
@app.route('/static/"index.html"')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)