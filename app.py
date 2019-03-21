# Allow configuration
import os

# Allow full utilisation of Flask framework
from flask import Flask, render_template, redirect, request, url_for

# Allow database manipulation
from flask_pymongo import PyMongo

# Allow working with _id fields
from bson.objectid import ObjectId

# Allow date and time manipulation
from datetime import datetime, timedelta

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'level-up'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds127115.mlab.com:27115/level-up'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_tracks')
def get_tracks():
    # Get the tracks collection
    tracks = mongo.db.tracks
    return render_template("tracks.html",
    tracks=tracks.find(), 
    )

@app.route('/sort_tracks_upvote_desc')
def sort_tracks_upvote_desc():
    tracks = mongo.db.tracks.aggregate(
           [
             { '$sort' : { 'upvotes' : -1} }
           ]
        )
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_upvote_asc')
def sort_tracks_upvote_asc():
    tracks = mongo.db.tracks.aggregate(
           [
             { '$sort' : { 'upvotes' : 1} }
           ]
        )
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_date_added_desc')
def sort_tracks_date_added_desc():
    tracks = mongo.db.tracks.aggregate(
           [
             { '$sort' : { 'date_added_raw' : -1} }
           ]
        )
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_date_added_asc')
def sort_tracks_date_added_asc():
    tracks = mongo.db.tracks.aggregate(
           [
             { '$sort' : { 'date_added_raw' : 1} }
           ]
        )
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/add_track')
def add_track():
    return render_template('add-track.html') 
    
@app.route('/insert_track', methods=['POST']) # Because you're using POST here, you have to set that via methods
def insert_track():
    # Format the timestamp that will be inserted into the record
    timestamp = datetime.now().strftime('%d %B %Y %H:%S')
    # Get the tracks collection
    tracks = mongo.db.tracks
    # Insert the record using the fields from the form on add-track.html
    tracks.insert_one(
        {
            'track_title': request.form.get('track_title'), # Access the tasks collection
            'artist': request.form.get('artist'),
            'youtube_link': request.form.get('youtube_link'),
            'year': request.form.get('year'),
            'genre': request.form.get('genre'),
            # Upvotes is set to 1 by default
            'upvotes': 1,
            'date_added': timestamp,
            'date_added_raw': datetime.now()
        }
    )
    return redirect(url_for('get_tracks')) # Once submitted, we redirect to the get_tasks function so that we can view our collection
    
@app.route('/upvote_track/<track_id>', methods=['POST'])
def upvote_track(track_id):
    tracks = mongo.db.tracks
    tracks.update( 
        {'_id': ObjectId(track_id)},
        # Increment the value of the upvote key by 1
        {'$inc': { 'upvotes': 1 }}
    )
    return redirect(url_for('get_tracks'))
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)