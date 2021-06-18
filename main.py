from flask import Flask , render_template, request, Response , stream_with_context
from camera import VideoCamera

import views
import dataSetCreator
import detector
import trainner
app = Flask(__name__)

app.add_url_rule('/', 'index', views.index)
app.add_url_rule('/index', 'index', views.index)
app.add_url_rule('/services', 'services', views.services)
app.add_url_rule('/ngo', 'ngo', views.ngo)
app.add_url_rule('/result', 'result', views.result)
app.add_url_rule('/services/upload', 'upload', views.upload)
app.add_url_rule('/services/search', 'search', views.search)

@app.route('/exec', methods=['GET','POST'])
def parse(name=None):
    if request.method == "POST":
        #get form data
        name = request.form.get('name')
        age = request.form.get('age')
        gen = request.form.get('gender')
        location = request.form.get('location')
    
    dataSetCreator.test(name, age, gen, location) 
    
    trainner.test()
    return render_template('services.html',name=name)

def gen(camera):
    while True:
        data= camera.get_frame()

        frame= data[0]
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/exec2')
def video_feed():
    return Response(stream_with_context(gen(VideoCamera())), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)