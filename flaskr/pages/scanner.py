from flask import Blueprint, render_template, Response, redirect, url_for, current_app
import io
import sys
import cv2
from pyzbar import pyzbar

bp = Blueprint('scanner', __name__, url_prefix="/scanner")

def gen():
    vc = cv2.VideoCapture(0)
    print(vc)
    while True:
        read_return_code, frame = vc.read()
        og = frame
        cv2.rectangle(frame, (200, 170), (450, 330), (0, 255, 100), 7)
        frame = cv2.flip(frame, 1)
        
        decode = pyzbar.decode(og)
        if decode is not None:
            print(decode)
            if len(str(decode)) > 10:
                global output
                output = str(decode).split("'")
                output = output[1]
                vc.release()
                return redirect(url_for('scanner.output', data=output))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        #print("a", file=sys.stderr)
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

@bp.route('/video_feed')
def video_feed():    
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@bp.route('/output/<int:data>')
def output(data):
    return str(data)

@bp.route('/scanner')
def scanner():
    return render_template('scanner/scanner.html')