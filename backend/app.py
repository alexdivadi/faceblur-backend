from pathlib import Path
from flask import Flask, request, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
import json
import os

from src.file import save, read_image
from src.face_detection import detect_img, obscure_faces, detect_video
from src.styles import BlurStyle

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    """
    Endpoint for getting face locations
    
    Method: POST
    Params: image: file, video: file, type: str
    """
    response = {}

    try:
        detect_type = request.form['type']

        if detect_type == 'image':
            file = request.files['image']

            img = read_image(file)
            faces = detect_img(img)

            response['faces'] = faces
            response['num_of_faces'] = len(faces)

        elif detect_type == 'video':
            file = request.files['video']
            name = secure_filename(file.filename)
            ext = Path(name).suffix

            uploaded_file = save(file, f'upload{ext}')
            faces = detect_video(uploaded_file)
            Path.unlink(uploaded_file)

            response['faces'] = [face.label for face in faces]
            response['num_of_faces'] = len(faces)

    except Exception as e:
        response['error'] = {
            'code': 500,
            'args': e.args,
        }

    return Response(json.dumps(response))

@app.route('/blur', methods=['POST'])
def blur():
    """
    Endpoint for obscuring faces
    
    Method: POST
    Params: image: file, video: file, type: str, style: str, detections: list[list[int]] as text
    """
    response = {}

    try:
        detect_type = request.form['type']

        if detect_type == 'image':
            file = request.files['image']
            name = secure_filename(file.filename)
            mimetype = file.content_type
            ext = Path(name).suffix

            img = read_image(file)
            detections: list = json.loads(request.form['detections'])
            style: BlurStyle = BlurStyle(request.form.get('style', default='blur'))
            
            data, h, w = obscure_faces(style, img, detections=detections, filetype=ext)
            data = base64.b64encode(data).decode() 

            response['img'] = data
            response['size'] = [w, h]
            response['mimetype'] = mimetype

        elif detect_type == 'video':
            pass

    except Exception as e:
        response['error'] = {
            'code': 500,
            'args': e.args,
        }

    return Response(json.dumps(response))


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))