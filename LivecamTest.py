from flask import Flask, render_template, Response, request, redirect, url_for, abort
import os,requests
import cv2
from gpiozero import MotionSensor
import time
from datetime import datetime as dt
from time import sleep
import threading
from multiprocessing import Process, Value
api = "dd2a2ba5e973832eb906fe9b5be2a8b7"
app = Flask(__name__)
pir = MotionSensor(4)
f = open("motionlog.txt", mode = "w")
output_lock = threading.Lock()
def live():  
    cam = cv2.VideoCapture('/dev/video0')
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
def motionlog():
    #f = open("motionlog.txt", mode = "w")
    f.write("Motion Detection Log" + "\n")
    while True:
            #output_lock.acquire()
            if pir.wait_for_motion():
                f.write("Motion Detected at "+ dt.now().strftime("%m_%d_%Y-%I:%M:%S_%p")+"\n")
                print('Motion Detected')
                sleep(5)
            elif pir.wait_for_no_motion():
                sleep(5)
                continue
            else:
                f.close
                #.release()
                break
    f.close            
@app.route('/')
def userlogin():
    return render_template('userlogin.html')

@app.route('/successful')
def successful_login():
    return render_template('successful_login.html')

@app.route('/processlogin', methods=['POST'])
def processlogin():
    if request.method == 'POST' and request.form['username'] == 'qq' and request.form['password'] == 'qq':
        return redirect(url_for("successful_login"))
    else:
        abort(401)

@app.route('/CameraImages', methods =['GET'])
def cam():
    return render_template("cameral.html")

@app.route('/newhome')
def newhome():
    return render_template("home.html")

@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/weather', methods =['GET'])
def home():
    construct_url = "https://api.openweathermap.org/data/2.5/weather?id=5224151&units=imperial&appid=" + api
    response = requests.get(construct_url)

    list_of_data = response.json()
    
    html_data = f"""

<!doctype html>
<html>
<head>
<center><h1><font color="#FFFFFF">Weather</font> <font color="#666CEC">API Data</font></h1></center>
</head>
<body bgcolor="#333333">
<center>
<table border="1" bordercolor="#666666">
    <tr style="color:white" bgcolor="#666CEC">
        <th>&ensp;Country Code&ensp;</th>
        <th>Coordinate</th>
        <th>&ensp;Temperature&ensp;</th>
        <th>&ensp;Pressure&ensp;</th>
        <th>&ensp;Humidity&ensp;</th>
        <th>&ensp;Windspeed&ensp;</th>
        <th>&ensp;Cloud Percentage&ensp;</th>
        <th>&ensp;Sunrise Time (UTM)&ensp;</th>
        <th>&ensp;Sunset Time (UTM)&ensp;</th>
    </tr>
    <tr style="color:white">
        <td><center>{str(list_of_data['sys']['country'])}</center></td>
        <td><center>{str(list_of_data['coord']['lon']) + ', ' 
                    + str(list_of_data['coord']['lat'])}</center></td>
        <td><center>{str(list_of_data['main']['temp']) + '&deg; F'}</center></td>
        <td><center>{str(list_of_data['main']['pressure']) + ' hPa'}</center></td>
        <td><center>{str(list_of_data['main']['humidity']) + '%'}</center></td>
        <td><center>{str(list_of_data['wind']['speed']) + ' mph'}</center></td>
        <td><center>{str(list_of_data['clouds']['all']) + '%'}</center></td>
        <td><center>{str(list_of_data['sys']['sunrise'])}</center></td>
        <td><center>{str(list_of_data['sys']['sunset'])}</center></td>
    </tr>
</table>
</center>
</body>
</html>
    """
    return html_data
    
@app.route('/livecam')
def livecam():
    return render_template('livecam.html')
    
@app.route('/Outdoor')
def Outdoor():
    return Response(live(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logtest')
def logtest():
    with open("motionlog.txt", "r") as f:
        content = f.read()
    return render_template("motionlog.html", content=content)
    
#with open("motionlog.txt", "r") as f:
#    content = f.read()
if __name__ == "__main__":
    #p = Process(target=motionlog)
    #p.start() 
    t1 = threading.Thread(target=motionlog)
    t1.start()
    app.run(port = 80,debug=True, host='131.128.51.187', use_reloader=False)
    #p.join()
    t1.join()

#f.close