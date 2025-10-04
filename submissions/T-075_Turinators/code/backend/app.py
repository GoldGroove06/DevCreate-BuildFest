# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify, send_file, Response,  send_from_directory
import os
from flask_cors import CORS
import test

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
CORS(app)
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World!!'

@app.route('/upload', methods=['POST'])
def upload():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    filename = video.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(save_path)
    print("Video saved at", save_path)
    output_path = test.process_video(filename, "best_new.pt")
    return jsonify({"url": f"http://localhost:5000/output/{output_path}"})


@app.route('/output/<filename>')
def serve_output(filename):
    print(filename)
    return send_file(os.path.join('outputs', filename), as_attachment=True)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True) 