from flask import Flask, render_template, Response
import os,requests
import cv2
#from gpiozero import MotionSensor
#import time
#from datetime import datetime as dt
#from time import sleep
api = "dd2a2ba5e973832eb906fe9b5be2a8b7"
app = Flask(__name__)
cam_test = cv2.VideoCapture(0)
#pir = MotionSensor(4)
#while True:
#    ret, frame = cam.read()
#    #ret, image = cam.read()
#    cv2.imshow('Video Test', frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        cam.release()
#        cv2.destroyAllWindows()
#        break
#    if pir.wait_for_motion():
#        cv2.imwrite('/home/pi/motion' + dt.now().strftime("%m_%d_%Y-%I:%M:%S_%p") + '.png', frame)
#        print('Movement Detected')
#    elif pir.wait_for_no_motion():
#        continue
#    else:
#        pir.wait_for_no_motion()
        
def live():  
    while True:
        success, frame = cam_test.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/', methods =['GET'])
def home():
    construct_url = "https://api.openweathermap.org/data/2.5/weather?q=Narragansett&appid=" + api
    response = requests.get(construct_url)

    list_of_data = response.json()
    
    html_data = f"""
    
    <table border="1">
    <tr>
        <td>Country Code</td>
        <td>Coordinate</td>
        <td>Temperature</td>
        <td>Pressure</td>
        <td>Humidity</td>
        <td>Windspeed</td>
        <td>Cloud Percentage</td>
        <td>Sunrise Time (UTC)</td>
        <td>Sunset Time (UTC)</td>
    </tr>
    <tr>
        <td>{str(list_of_data['sys']['country'])}</td>
        <td>{str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat'])}</td>
        <td>{str(list_of_data['main']['temp']) + 'k'}</td>
        <td>{str(list_of_data['main']['pressure']) + 'atm'}</td>
        <td>{str(list_of_data['main']['humidity']) + 'g/m3'}</td>
        <td>{str(list_of_data['wind']['speed']) + 'm/s'}</td>
        <td>{str(list_of_data['clouds']['all']) + '%'}</td>
        <td>{str(list_of_data['sys']['sunrise']) + 'UTM'}</td>
        <td>{str(list_of_data['sys']['sunset']) + 'UTM'}</td>
    </tr>

</table>
    """
    return html_data

@app.route('/CameraImages', methods =['GET'])
#def cam():
#    image_names = os.listdir('/home/pi/motion')
#    render_template('home.html', image_name=image_names)
#    return render_template("photos.html")
        
@app.route('/Outdoor')
def Outdoor():
    return Response(live(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(port = 80,debug=True, host='131.128.51.187')