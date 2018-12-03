from flask import Flask,jsonify, request, render_template
from tables import SensorReading, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True
app.config.update(JSONIFY_MIMETYPE='application/json')
STORE_TO_DB = False
Session = None

if STORE_TO_DB:
    db_user = 'amitr'
    db_pass = 'pymetawear'
    db_name = 'metawear'
    db_port = '3306'
    sql_engine = create_engine('mysql+pymysql://'+db_user+':'+db_pass+'@localhost:'+db_port+'/'+db_name,
                               pool_recycle=3600,
                               echo=True)
    Session = sessionmaker(bind=sql_engine)
    Base.metadata.create_all(sql_engine)


@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    accel = data['accel']
    gyro = data['gyro']
    print("Data recieved = ", len(accel), len(gyro))

    if STORE_TO_DB:
        cur_readings = []
        for i in range(len(accel)):
            cur_readings.append(SensorReading(sensor_type="AC", data=str(accel[i]['value']),
                                        time=str(accel[i]['epoch'])))
        for i in range(len(gyro)):
            cur_readings.append(SensorReading(sensor_type="GY", data=str(gyro[i]['value']),
                                              time=str(gyro[i]['epoch'])))

        cur_session = Session()
        cur_session.add_all(cur_readings)
        cur_session.commit()
        cur_session.close()
    return 'Data received', 200


@app.route('/echo_error', methods=['GET'])
def echo_error():
    print("Error occurred in client, must be connection issue with metawear")

    return 'Done', 200

