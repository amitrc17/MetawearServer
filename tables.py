from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
Base = declarative_base()


class SensorReading(Base):
    __tablename__ = 'sensorreadings'

    reading_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    device = Column(Integer)  # 0->spire tag, 1->watch, 2->metawear
    sensor_type = Column(Integer)  # 0->Accel, 1->Gyro, 2->heart_rate, 3->resp_rate 4->steps
    data = Column(String(100))  # Each dimension of data is separated by a ~ (tilde)
    time = Column(String(20))  # Unix timestamp (millis from 1970)

    def __repr__(self):
        return '<SensorReadings(user_id="%s", device="%s", sensor_type="%s", data="%s", time="%s")>' % (
            self.user_id,
            self.device,
            self.sensor_type,
            self.data,
            self.time)


class Homes(Base):
    __tablename__ = 'homes'

    home_id = Column(Integer, primary_key=True)
    child_id = Column(String)
    parent_id = Column(String)
    device_ip = Column(String(30))

    def __repr__(self):
        return '<Homes(home_id="%s", child_id="%s", parent_id="%s", device_ip="%s")>' % (
            self.home_id,
            self.child_id,
            self.parent_id,
            self.device_ip)


class Tantrums(Base):
    __tablename__ = 'tantrums'

    tantrum_id = Column(Integer, primary_key=True)
    parent_id = Column(String(20))
    start_timestamp = Column(String(20))
    end_timestamp = Column(String(20))

    def __repr__(self):
        return '<Tantrums(trantrum_id="%s", parent_id="%s", start_timestamp="%s", end_timestamp="%s")>' % (
            self.tantrum_id,
            self.parent_id,
            self.start_timestamp,
            self.end_timestamp)