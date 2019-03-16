import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'level-up'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds127115.mlab.com:27115/level-up'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get-tracks')
def get_tasks():
    return render_template("tracks.html",
    tracks=mongo.db.tracks.find())
    
@app.route('/add-track')
def add_track():
    return render_template('add-track.html') 
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)