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
    # This is used within tracks.html to determine whether to show the 'next' button
    # It would not make sense to show the next button if there are no more tracks to view
    tracks_col_count = tracks_collection.count() 
    
    
    # hold_pagination will only ever be in session if the user has come from a url where it makes sense to keep the pagination
    # Pagination is held for next_tracks, prev_tracks, upvote_track and edit_track
    # In which case, ensure the pagination value currently in the session is used to show the user the correct tracks
    if 'hold_pagination' in session:
        pagination = session['pagination']
    # If hold_pagination does not exist, this means the user has come to tracks.html some other way, presumably by refreshing the page or clicking a nav link
    # This means the pagination should be set to 0 to ensure the user is seeing the first top 5 tracks
    else:
        session['pagination'] = 0
        pagination = session['pagination']
        
    # Delete the hold_pagination session.
    # If this session is needed again, it will be created by either upvote_track, next_tracks or prev_tracks
    # For all other use cases it is redundant
    session.pop('hold_pagination', None)
    
    # Sort the tracks collection by upvotes with the highest upvoted track first. Limit to 5 results
    tracks = tracks_collection.find().sort(
                                            'upvotes', pymongo.DESCENDING).skip(
                                                                                pagination).limit(5)
    
    return render_template("tracks.html", 
                            tracks = tracks,
                            pagination = pagination,
                            tracks_col_count = tracks_col_count
                            )
                            
@app.route('/next_tracks')
def next_tracks():
    session['pagination'] += 5
    session['hold_pagination'] = True
    
    return redirect(url_for('get_tracks'))
                            
@app.route('/prev_tracks')
def prev_tracks():
    session['pagination'] -= 5
    session['hold_pagination'] = True
    
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
    
    session['hold_pagination'] = True
    
    return redirect(url_for('get_tracks'))
    
@app.route('/edit_track/<track_id>')
# This function essential gets the task that matches this task id
def edit_track(track_id):
    # So we want to find one particular task from the task collection
    # We're looking for a match for the ID
    # We wrap task_id with ObjectId in order to make it a format acceptable to mongodb
    the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
    # We also need a list of all the categories in order to populate the edit form
    # all_cats = mongo.db.categories.find()
    session['hold_pagination'] = True
    # Render edit_task.html and pass across the_task and cats
    # REMEMBER TO ASSIGN CAT = THE_CAT (OR MAYBE GENRE = THE_GENRE) IF YOU MAKE GENRES INTO A DROPDOWN
    return render_template('edit-track.html', track = the_track)
    
@app.route('/insert_edited_track/<track_id>', methods=["POST"])
def insert_edited_track(track_id):
    # Get the tracks collection
    tracks = mongo.db.tracks
    
    # In order for the edit to work properly, some values that the user should not be eligible to update (e.g. upvotes) need to be retrieved from the the database prior to update
    # If not, update will delete any old key/values that aren't explicitly passed through with the update
    # In order to do this, find() is used to grab a cursor of the track being edited
    old_values = tracks.find({"_id": ObjectId(track_id)})
    
    # Loop through the cursor and get the values the user shouldn't be able to change
    # Once tracks.update occurs, any values not specified within the update won't be added to the database
    # That would mean the track would lose its upvotes, date_added and date_added_raw
    for item in old_values:
        upvotes = item['upvotes']
        date_added = item['date_added']
        date_added_raw = item['date_added_raw']
    
    # Do the update
    tracks.update( {'_id': ObjectId(track_id)},
    {
        'track_title':request.form.get('track_title'),
        'artist':request.form.get('artist'),
        'youtube_link': request.form.get('youtube_link'),
        'year': request.form.get('year'),
        'genre':request.form.get('genre'),
        # These last three are the same values as what were created when the track was added to the database initially
        'upvotes': upvotes,
        'date_added': date_added,
        'date_added_raw': date_added_raw
    })
    return redirect(url_for('get_tracks'))
    
@app.route('/delete_track/<track_id>')
def delete_track(track_id):
    # Use ObjectId to parse the task_id in a format acceptable to mongo
    mongo.db.tracks.remove({'_id': ObjectId(track_id)})
    session['hold_pagination'] = True
    # Then go to the get_tasks function
    return redirect(url_for('get_tracks'))
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)