from flask import Flask, render_template, request, redirect, url_for, Response
from modules import vingertellen, kleurenherkenning
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)


def gen_raw():
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_processed(processor):
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        frame = processor(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


def get_processor(name):
    if name == "vingertellen":
        return vingertellen.count_fingers
    elif name == "kleurenherkenning":
        return kleurenherkenning.detect_color
    else:
        return lambda frame: frame


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/functie/<naam>')
def functie(naam):
    return render_template('result.html', functie=naam)

@app.route('/video_feed/raw')
def video_feed_raw():
    return Response(gen_raw(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/<naam>')
def video_feed_processed(naam):
    processor = get_processor(naam)
    return Response(gen_processed(processor), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
