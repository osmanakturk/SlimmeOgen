from flask import Flask, render_template, request, redirect, url_for, Response
from modules import vingertellen, kleurenherkenning, bewegend_tekenen
import cv2

app = Flask(__name__)




#def gen_raw():
#    camera = cv2.VideoCapture(0)
#    while True:
#        success, frame = camera.read()
#        if not success:
#            break
#        frame = cv2.flip(frame, 1)
#        _, buffer = cv2.imencode('.jpg', frame)
#        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_processed(processor):
    #camera = cv2.VideoCapture('/dev/video0') # for raspberry pi
    camera = cv2.VideoCapture(0)
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
    elif name == "bewegend-tekenen":
        return bewegend_tekenen.bewegend_tekenen
    else:
        return lambda frame: frame


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/functie/<naam>')
def functie(naam):
    return render_template('result.html', functie=naam)

#@app.route('/video_feed/raw')
#def video_feed_raw():
#    return Response(gen_raw(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/result/<naam>')
def result_text(naam):
    if naam == "vingertellen":
        return vingertellen.get_result()
    elif naam == "kleurenherkenning":
        return kleurenherkenning.get_result()
    else:
        return "No result"

@app.route('/video_feed/<naam>')
def video_feed_processed(naam):
    processor = get_processor(naam)
    return Response(gen_processed(processor), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
