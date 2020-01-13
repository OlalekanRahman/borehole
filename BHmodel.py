from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()
class borehole(Base):
    __tablename__="borehole"
    id = Column(Integer, primary_key=True)
    category =Column(String(),nullable=False)
    sub_date=Column(String(),nullable=False)
    lat=Column(Float(),nullable=False,unique=True)
    long=Column(Float(),nullable=False,unique=True)
    addr=Column(String(100),nullable=False)
    def __repr__(self):
        return '<Borehole: Category=%r,latitude=%0.4f,longitude=%0.4f,Address=%r>' % (self.category,self.lat,self.long,self.addr)