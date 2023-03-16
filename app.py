from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess

app = Flask(__name__)


uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    subprocess.run("ls", shell=True)
    subprocess.run(['py', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))], shell=True)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    return obj

@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['py', 'detect.py', '--source', 'rtsp://admin:anas1155@46.152.196.211:554/Streaming/Channels/1/'], shell=True)
    return "done"
 

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)

# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_operation(op_name):
    docs = db.collection('ai_operation').get()

    for doc in docs:
        # Extract the 'aiop_name' and 'aiop_id' from each dictionary
        aiop_name = doc.to_dict()['aiop_name']
        aiop_id = doc.to_dict()['aiop_id']

        # Print the extracted values
        #print(f"aiop_name: {aiop_name}, aiop_id: {aiop_id}")
        if op_name == aiop_name:
            return aiop_id


def get_id_of_cam(id_op):
    docs = db.collection('aiop_camera').get()

    for doc in docs:
        # Extract the 'aiop_id' and 'cam_id' from each dictionary
        aiop_id = doc.to_dict()['aiop_id']
        cam_id = doc.to_dict()['cam_id']

        # Print the extracted values
        #print(f"aiop_id: {aiop_id}, cam_id: {cam_id}")
        if id_op == aiop_id:
            return cam_id


def get_url_of_cam(url_of_cam):
    docs = db.collection('camera').get()

    for doc in docs:
        # Extract the 'aiop_name' and 'aiop_id' from each dictionary
        cam_id = doc.to_dict()['cam_id']
        cam_url = doc.to_dict()['cam_url']

        # Print the extracted values
        #print(f"cam_id: {cam_id}, cam_url: {cam_url}")
        if url_of_cam == cam_id:
            return cam_url


def get_id_of_obj(id_obj):
    docs = db.collection('aiop_obj').get()

    for doc in docs:
        # Extract the 'aiop_id' and 'cam_id' from each dictionary
        aiop_id = doc.to_dict()['aiop_id']
        obj_id = doc.to_dict()['obj_id']

        # Print the extracted values
        #print(f"aiop_id: {aiop_id}, obj_id: {obj_id}")
        if id_obj == aiop_id:
            return obj_id



def get_name_of_obj(id_name_of_obj):
    docs = db.collection('object').get()

    for doc in docs:
        # Extract the 'aiop_id' and 'cam_id' from each dictionary
        obj_id = doc.to_dict()['obj_id']
        obj_name = doc.to_dict()['obj_name']

        # Print the extracted values
        #print(f"obj_id: {obj_id}, obj_name: {obj_name}")
        if id_name_of_obj == obj_id:
            return obj_name

if __name__ == '__main__':

    id_of_op = get_operation('OD50')
    print(id_of_op)
    id_of_cam = get_id_of_cam(id_of_op)
    print(id_of_cam)
    url_of_cam = get_url_of_cam(id_of_cam)
    print(url_of_cam)
    id_of_obj = get_id_of_obj(id_of_op)
    print(id_of_obj)
    name_of_obj = get_name_of_obj(id_of_obj)
    print(name_of_obj)


    app.run(debug=True, host='0.0.0.0')