# cd .\firebase_storage_python_flutter-main\
# cd .\video_analyzer_flutter\
# flutter run --no-sound-null-safety
# New terminal for server.py
# python server.py
# cd .\firebase_storage_flask\
import os
from flask import Flask, request,abort,jsonify
import ai_engine
import important

# flutter run --no-sound-null-safety
# Server is the "bridge" between frontend and backend

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.mov'] # decides what FORMAT media that user can upload to server

@app.route('/analize', methods=['GET', 'POST']) # route for uploading image, when analyze video button is clicked, direct to ResultPage.dart
def edit_video():
    uploaded_video = request.files.getlist("video1")[0] # Getting the files from frontend (video1) to use in the backend
    uploaded_video2 = request.files.getlist("video2")[0] # Getting the files from frontend (video2) to use in the backend
    print(uploaded_video.filename)
    print(uploaded_video2.filename)
    video1_filename = uploaded_video.filename # stores file name (coach sample)
    video2_filename = uploaded_video2.filename # stores file name (student sample)
    if video1_filename != '' and video2_filename != '': # checks if the user inserted a video
        
        _, video_file_ext = os.path.splitext(video1_filename)
        _, image_file_ext = os.path.splitext(video2_filename)
        if image_file_ext not in app.config['UPLOAD_EXTENSIONS'] or video_file_ext not in app.config[
            'UPLOAD_EXTENSIONS']: # checks if video file is mp4
            abort(400)
        #Save video1 and video2
        
        uploaded_video.save(video1_filename) # takes uploaded video from frontend to saved in python project file (saved), imagepicker videos
        uploaded_video2.save(video2_filename) # takes uploaded video from frontend to saved in python project file

        # You'll use the video1_path and video2_path to run the AI Engine
        # Call the function to run the AI Engine and returns the list of links to be access in the FrontEnd(Flutter APP)
        
        
        links = ai_engine.send_images_example(video1_filename,video2_filename) # References ai_engine
        
        if(video1_filename != ''): 
            os.remove(video1_filename)
            os.remove(video2_filename)
        
        return jsonify(links) # sending back the picture links to frontend, vid 1 vid 2 files deleted


if __name__ == "__main__":
    app.run()