from flask import Flask, url_for, render_template, jsonify
import pymssql
from collections import defaultdict
from os import getenv
app = Flask(__name__)

db=pymssql.connect(server='', user='', password='Mla14782', database='')
@app.route("/")
def hello():
    return "Hello, you're connected to the Cloud Jammer Database!"

@app.route("/juices")
def juices(): 
    cursor=db.cursor()
    cursor.execute("SELECT TOP 10 * FROM juices;")
    row=cursor.fetchone()
    t= row[1]
    print(t)
    return render_template("test.html", test=t)

##Find if a juice flavor is within the system
@app.route("/juices/<juice>")
def juice_lookup(juice): 
    cursor=db.cursor(as_dict=True)
    cursor.execute("SELECT * FROM juices WHERE flavor=%s", juice)
    row=cursor.fetchone()
    return jsonify(row)

##Find the juices that exist with the specified store
@app.route("/juices/<store>")
def store_lookup(store):
    cursor=db.cursor(as_dict=True)
    storeNew = "inventory."+store
    print(storeNew)
    if(store.upper() == 'YORK'):
        cursor.execute("SELECT juices.juiceID, juices.brand, juices.flavor FROM juices INNER JOIN inventory ON juices.juiceID=inventory.juiceID WHERE inventory.YORK='TRUE'")
    if(store.upper() == 'GETTYSBURG'):
        cursor.execute("SELECT juices.juiceID, juices.brand, juices.flavor FROM juices INNER JOIN inventory ON juices.juiceID=inventory.juiceID WHERE inventory.GETTYSBURG='TRUE'")
    if(store.upper() == 'LEMOYNE'):
        cursor.execute("SELECT juices.juiceID, juices.brand, juices.flavor FROM juices INNER JOIN inventory ON juices.juiceID=inventory.juiceID WHERE inventory.LEMOYNE='TRUE'")
    if(store.upper() == 'FREDERICK'):
        cursor.execute("SELECT juices.juiceID, juices.brand, juices.flavor FROM juices INNER JOIN inventory ON juices.juiceID=inventory.juiceID WHERE inventory.FREDERICK='TRUE'")

    row=cursor.fetchall()
    return jsonify(row)

if __name__ == "__main__":
    app.run(
        host="192.168.1.241",
        port=int("80"),
        debug=True
    )