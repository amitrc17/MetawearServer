from flask import Flask, request
from tables import SensorReading, Homes, Tantrums, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.debug = True
app.config.update(JSONIFY_MIMETYPE='application/json')
STORE_TO_DB = False
Session = None
STUDY_EMAIL_ID = 'tantrumwatchumass@gmail.com'
STUDY_EMAIL_PASSWORD = 'tantrumwatch@123'

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
    u_id = data['user_id']
    device = data['device']
    sensor_types = ['accel', 'gyro', 'heart_rate', 'resp_rate', 'steps']

    if STORE_TO_DB:
        cur_readings = []
        for sensor_index, sensor_type in enumerate(sensor_types):
            if sensor_type in data:
                for reading_index in range(len(data[sensor_type])):
                    cur_readings.append(SensorReading(user_id=u_id, device=device, sensor_type=sensor_index,
                                                      data=str(data[sensor_type][reading_index]['value']),
                                                      time=str(data[sensor_type][reading_index]['epoch'])))

        cur_session = Session()
        cur_session.add_all(cur_readings)
        cur_session.commit()
        cur_session.close()
        print('Successfully stored data to DB')
    else:
        print('Data not being stored to DB, to turn on data storage change config entry "STORE_TO_DB" to True')

    return 'Data received', 200


@app.route('/register_home', methods=['POST'])
def register_home():
    data = request.get_json()
    child_id = data['child_id']
    parent_id = data['parent_id']
    device_ip = data['device_ip']

    home = Homes(child_id=child_id, parent_id=parent_id, device_ip=device_ip)

    if STORE_TO_DB:
        cur_session = Session()
        cur_session.add(home)
        cur_session.commit()
        cur_session.close()
        print('Successfully registered home, stored to DB')
    else:
        print('Data not being stored to DB, to turn on data storage change config entry "STORE_TO_DB" to True')

    print('The home object is = ', home)
    return 'Register Success', 200


@app.route('/record_tantrum', methods=['POST'])
def record_tantrum():
    data = request.get_json()
    parent_id = data['parent_id']
    start_time = data['start_time']
    end_time = data['end_time']

    tantrum = Tantrums(parent_id=parent_id, start_timestamp=start_time, end_timestamp=end_time)

    if STORE_TO_DB:
        cur_session = Session()
        cur_session.add(tantrum)
        cur_session.commit()
        cur_session.close()
        print('Successfully recorded tantrum')
    else:
        print('Data not being stored to DB, to turn on data storage change config entry "STORE_TO_DB" to True')

    print('The tantrum object is = ', tantrum)
    return 'Successfully recorded tantrum', 200


@app.route('/generate_feedback_form', methods=['GET'])
def generate_feedback_form():
    data = request.get_json()
    parent_id = data['parent_id']
    feedback_date = datetime.fromtimestamp(int(data['feedback_timestamp'])).date()

    cur_session = Session()
    tantrums = cur_session.query(Tantrums).filter(Tantrums.parent_id == parent_id).all()

    todays_tantrums = [tantrum for tantrum in tantrums
                       if datetime.fromtimestamp(tantrum.start_timestamp).date() == feedback_date]

    # Send email to Parent-Id from STUDY_EMAIL_ID
    # TODO: Check if we can do this without logging in every time
    msg = get_email_body(todays_tantrums, parent_id, feedback_date)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(STUDY_EMAIL_ID, STUDY_EMAIL_PASSWORD)
    smtp_server.sendmail(STUDY_EMAIL_ID, [parent_id], msg)

    return 'Done', 200


@app.route('/echo_error', methods=['GET'])
def echo_error():
    print("Error occurred in client, must be connection issue with metawear")

    return 'Done', 200


@app.route('/', methods=['GET'])
def index():
    return 'Server is up', 200


# TODO: Move this method into a helper/utilities file
def get_email_body(tantrums, parent_id, feedback_date):
    if len(tantrums) == 0:
        msg_text = 'Hi,\n\nGood Job! There have been no tantrums today! :) \n\n Thank You!'
    else:
        msg_text = 'Hi,\n\nYou have reported tantrums at the following times today - \n\n'
        for tantrum in tantrums:
            msg_text = msg_text + str(datetime.fromtimestamp(tantrum.start_timestamp)) + \
                       ' to ' + str(datetime.fromtimestamp(tantrum.end_timestamp)) + '\n'
        msg_text = msg_text + '\nCould you please provide remarks for these tantrums at the link given below? \n'
        # TODO: Add link to form
        msg_text = msg_text + '\n\nThank You!'
    msg = MIMEText(msg_text)
    msg['From'] = STUDY_EMAIL_ID
    msg['To'] = parent_id
    msg['Subject'] = 'Tantrum Remarks For ' + str(feedback_date)
    return msg

