from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
Base = declarative_base()


class SensorReading(Base):
    __tablename__ = 'sensorreadings'

    reading_id = Column(Integer, primary_key=True)
    sensor_type = Column(String(2))
    data = Column(String(100))
    time = Column(String(25))

    def __repr__(self):
        return '<SensorReadings(data="%s", time="%s")>' % (
            self.data,
            self.time)
