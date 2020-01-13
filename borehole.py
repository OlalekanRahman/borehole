DATABASE_URI = 'postgres+psycopg2://postgres:iseyin2018@localhost:5432/postgres'
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URI)
from BHmodel import *
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
from flask import Flask,redirect,request,render_template
import string,json
app1=Flask(__name__)
Session = sessionmaker(bind=engine)
categories = ['public','private']
def sanitize_string(userinput):
    whitelist = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm !?$.,;/|\:-'()&"
    s=list(filter(lambda x: x in whitelist, userinput))
    s=''.join(s)
    if s == '':
        return 'No address attached'
    return s
def get_data(w):
    BHwells=[]
    for i in w:
        BHwells.append({"category":i.category,"Address":i.addr})
    return json.dumps(BHwells)
@app1.route('/')
def map_():
    s=Session()
    wells = s.query(borehole).all()
    wells=get_data(wells)
    return render_template("bhm.html",wells=wells,categories=categories)
@app1.route("/submitwell", methods=['get','POST'])
def submitwell():
    s=Session()
    category = request.form.get("category")
    if category not in categories:
        return 'Wrong value entered'
    try:
        sdate = request.form.get("date")
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
        address = sanitize_string(request.form.get("address"))
    except:
         return '<h2>Error in values  =>> <a href="/">Go back to map page<a></h2>'
    try:
        bh=borehole(category=category, sub_date=sdate, lat=latitude, long=longitude,addr=address)
        s.add(bh)
        s.commit()
    except:
        return '<h2>Error in inputs to DB =>> <a href="/">Go back to map page<a></h2>'
    return '<h1>Well submitted!!! ==>> <a href="/">Go back to map page<a></h1>'
    
if __name__ == "__main__":
    app1.run(port=5000, debug=False)