# Allow configuration
import os

# Allow full utilisation of Flask framework
from flask import Flask, render_template, redirect, request, url_for, session

# Allow database manipulation
from flask_pymongo import PyMongo, pymongo

# Allow working with _id fields
from bson.objectid import ObjectId

# Allow date and time manipulation
from datetime import datetime, timedelta

# Initialise Flask
app = Flask(__name__)
# Connect to Database
app.config["MONGO_DBNAME"] = 'level-up'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds127115.mlab.com:27115/level-up'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Initialise PyMongo
mongo = PyMongo(app)

# Index Route
@app.route('/index')
@app.route('/')
def index():
    # Clear any session the user may have 
    # This ensures the user can go to get_tracks cleanly
    session.clear()
    tracks = mongo.db.tracks
    title = "DesertIsland | Home"
    return render_template("index.html", 
                            tracks = tracks.aggregate(
                                                       [
                                                         { '$sort' : { 'upvotes' : -1} }
                                                       ]
                                                    ),
                            title = title
                            )

@app.route('/about')
def about():
    title = "DesertIsland | About"
    return render_template("about.html", title = title)

@app.route('/get_tracks')
def get_tracks():
    # Get the tracks collection
    tracks_collection = mongo.db.tracks
    # Get the number of items in tracks_collection
    tracks_col_count = tracks_collection.count()
    
    # Get the item with the max upvotes
    max_upvotes = tracks_collection.find().sort('upvotes', pymongo.DESCENDING).limit(1)
    # Get the item with the min upvotes
    min_upvotes = tracks_collection.find().sort('upvotes', pymongo.ASCENDING).limit(1)
    
    offset = 3
    
    # Set the limit for the number of tracks returned
    limit = 2
    
    def determine_origin():
        # This ensures that the session for just_upvoted is defined
        # If it isn't defined, a keyerror will result when the user is taken to get_tracks
        if 'just_upvoted' not in session:
            session['just_upvoted'] = False
        # If the user has just come from upvoting a track
        elif session['just_upvoted']:
            # Set just_upvoted to true
            just_upvoted = session['just_upvoted']
        elif not session['just_upvoted']:
            return
        else:
            # Else the user has not come from upvoting a track
            # This means they are fresh coming to tracks.html or they have clicked refresh
            session['pagination'] = 0
            
    determine_origin()
        
    # Whatever the outcome of the if statement above, assign pagination to the value of session.pagination
    pagination = session['pagination']
    
    # Reset the just_upvoted session. This ensures pagination gets wiped ready to start afresh
    session['just_upvoted'] = False
        
    session['ranking'] = [1,2,3,4,5]
    ranking = session['ranking']
    
    starting_track = tracks_collection.find().sort('upvotes', pymongo.DESCENDING)
    last_track = starting_track[offset]['upvotes']
    
    # Sort the tracks collection by upvotes with the highest upvoted track first. Limit to 5 results
    tracks = tracks_collection.find().sort(
                                            'upvotes', pymongo.DESCENDING).skip(
                                                                                pagination).limit(5)
                                                                                
    
    return render_template("tracks.html", 
                            tracks = tracks,
                            pagination = pagination,
                            ranking = ranking
                            )
                            
@app.route('/next_tracks')
def next_tracks():
    session['pagination'] += 5
    
    return redirect(url_for('get_tracks'))
                            
@app.route('/prev_tracks')
def prev_tracks():
    session['pagination'] -= 5
    
    return redirect(url_for('get_tracks'))

@app.route('/sort_tracks_upvote_desc')
def sort_tracks_upvote_desc():
    tracks = mongo.db.tracks.find().sort('upvotes', pymongo.DESCENDING)
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_upvote_asc')
def sort_tracks_upvote_asc():
    tracks = mongo.db.tracks.find().sort('upvotes', pymongo.ASCENDING)
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_date_added_desc')
def sort_tracks_date_added_desc():
    tracks = mongo.db.tracks.find().sort('date_added_raw', pymongo.DESCENDING)
    return render_template("tracks.html", tracks=tracks)
    
@app.route('/sort_tracks_date_added_asc')
def sort_tracks_date_added_asc():
    tracks = mongo.db.tracks.find().sort('date_added_raw', pymongo.ASCENDING)
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
    
    session['just_upvoted'] = True
    
    return redirect(url_for('get_tracks'))
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)