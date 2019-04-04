# NEEDED ONLY FOR PRINTS
from __future__ import print_function
import sys

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

# Secret key is needed in order to use session variables
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Initialise PyMongo
mongo = PyMongo(app)

# # GLOBAL VARIABLES
# """These are kept here to make things easier to change/update"""
# # Pagination

# Index Route
"""
This is the default route
Render the home page
Grab the current top 3 tracks by upvotes and display them on the home page
"""
@app.route('/index')
@app.route('/')
def index():
    # Clear any session variables the user may have 
    # This ensures the user can go to get_tracks cleanly
    session.clear()
    # Get the tracks collection
    tracks = mongo.db.tracks.find()
    # Set the html title
    title = "DesertIsland | Home"
    return render_template("index.html", 
                            # Sort all tracks by upvotes descending, limit to 3 results
                            tracks = tracks.sort(
                                                'upvotes', pymongo.DESCENDING).limit(3),
                            title = title
                            )

@app.route('/about')
def about():
    title = "DesertIsland | About"
    return render_template("about.html", title = title)
    
@app.route('/track_detail/<decade_filter>/<sorting_order>/<track_id>')
def track_detail(decade_filter, sorting_order, track_id):
    title = "DesertIsland | About"
    # Grab the track_id from what was passed through
    the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
    return render_template("track-detail.html", title = title, decade_filter = decade_filter, sorting_order = sorting_order, track = the_track)

@app.route('/get_tracks/<decade_filter>/<int:sorting_order>', methods = ['POST','GET'])
def get_tracks(decade_filter, sorting_order):
    """
    This function renders the tracks on tracks.html
    Tracks can be sorted and filtered by various criteria
    The filter and sort values are passed into the function from other functions which redirect to here
    """
    # Get the tracks collection
    tracks_collection = mongo.db.tracks

    # hold_pagination will only ever be in session if the user has come from a url where it makes sense to keep the pagination of content
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
    # If this session is needed again, it will be created by the appropriate function
    # For all other use cases it is redundant
    session.pop('hold_pagination', None)
    
    if decade_filter == "pre1950":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 2010}}, 
                                {"year": {'$lt': 2020}}
                                ]
                        })
    elif decade_filter == "1950s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1950}}, 
                                {"year": {'$lt': 1960}}
                                ]
                        })
    elif decade_filter == "1960s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1960}}, 
                                {"year": {'$lt': 1970}}
                                ]
                        })
    elif decade_filter == "1970s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1970}}, 
                                {"year": {'$lt': 1980}}
                                ]
                        })
    elif decade_filter == "1980s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1980}}, 
                                {"year": {'$lt': 1990}}
                                ]
                        })
    elif decade_filter == "1990s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1990}}, 
                                {"year": {'$lt': 2000}}
                                ]
                        })
    elif decade_filter == "2000s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 2000}}, 
                                {"year": {'$lt': 2010}}
                                ]
                        })
    elif decade_filter == "2010s":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 2010}}, 
                                {"year": {'$lt': 2020}}
                                ]
                        })
    else:
        tracks_decade = tracks_collection.find()
    
    # The sorting_order variable is used to determine how to sort the tracks
    # sorting_order = 1 means sort tracks by HIGHEST UPVOTES. This is the default sorting order
    # sorting_order = 2 means sort tracks by LOWEST UPVOTES first
    # sorting_order = 3 means sort tracks by date added to the database with the LATEST date first
    # sorting_order = 4 means sort tracks by date added to the databse with the OLDEST date first
    if sorting_order == 1:
        # Find all tracks within the tracks collection. Sort by upvotes descending, skip using the value of pagination and limit
        tracks = tracks_decade.sort(
                                                'upvotes', pymongo.DESCENDING).skip(
                                                                                    pagination).limit(5)
    elif sorting_order == 2:
        # Find all tracks within the tracks collection. Sort by upvotes ascending, skip using the value of pagination and limit
        tracks = tracks_decade.sort(
                                            'upvotes', pymongo.ASCENDING).skip(
                                                                                pagination).limit(5)
    elif sorting_order == 3:
         # Find all tracks within the tracks collection. Sort by date_added_raw descending, skip using the value of pagination and limit
        tracks = tracks_decade.sort(
                                            'date_added_raw', pymongo.DESCENDING).skip(
                                                                                pagination).limit(5)
    elif sorting_order == 4:
        # Find all tracks within the tracks collection. Sort by date_added_raw ascending, skip using the value of pagination and limit
        tracks = tracks_decade.sort(
                                            'date_added_raw', pymongo.ASCENDING).skip(
                                                                                pagination).limit(5)
                                                                                
    # Get the number of tracks as currently defined by the filtering
    # This is used within tracks.html to determine whether to show the 'next' button
    # It would not make sense to show the next button if there are no more tracks to view                                                                          
    tracks_count = tracks.count() 

    # Render tracks.html
    # tracks is the list of tracks to be rendered
    # sorting_order is how they are to be sorted (corresponding to the system in the if/else statement above)
    # pagination determines how many tracks are to be skipped. The user navigates through the pagination using the next and previous buttons on tracks.html
    # tracks_col_count determines whether to hide the next and previous buttons. If the user has reached the end of the list it doesn't make sense and would be confusing for them to be able to click 'Next'
    return render_template("tracks.html", 
                            tracks = tracks,
                            decade_filter = decade_filter,
                            sorting_order = sorting_order,
                            pagination = pagination,
                            tracks_count = tracks_count
                            )
                            

@app.route('/next_tracks/<decade_filter>/<int:sorting_order>')
def next_tracks(decade_filter, sorting_order):
    """
    This function takes the user to the next 5 tracks, determined by the pagination the user is currently on, the sorting order they are currently using as well as the filtering options set
    """
    session['pagination'] += 5
    session['hold_pagination'] = True
    
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
                            
@app.route('/prev_tracks/<decade_filter>/<int:sorting_order>')
def prev_tracks(decade_filter, sorting_order):
    """
    This function takes the user to the previous 5 tracks, determined by the pagination the user is currently on, the sorting order they are currently using as well as the filtering options set
    """
    session['pagination'] -= 5
    session['hold_pagination'] = True
    
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))

@app.route('/sort_tracks_upvote_desc/<decade_filter>')
def sort_tracks_upvote_desc(decade_filter):
    """
    Change the sorting order to show tracks with HIGHEST upvotes first. This is the default sorting order
    """
    return redirect(url_for('get_tracks', sorting_order = 1, decade_filter = decade_filter))
    
@app.route('/sort_tracks_upvote_asc/<decade_filter>')
def sort_tracks_upvote_asc(decade_filter):
    """
    Change the sorting order to show tracks with LOWEST upvotes first
    """
    return redirect(url_for('get_tracks', sorting_order = 2, decade_filter = decade_filter))
    
@app.route('/sort_tracks_date_added_desc/<decade_filter>')
def sort_tracks_date_added_desc(decade_filter):
    """
    Change the sorting order to show NEWEST tracks by date added first
    """
    return redirect(url_for('get_tracks', sorting_order = 3, decade_filter = decade_filter))
    
@app.route('/sort_tracks_date_added_asc/<decade_filter>')
def sort_tracks_date_added_asc(decade_filter):
    """
    Change the sorting order to show OLDEST tracks by date added first
    """
    return redirect(url_for('get_tracks', sorting_order = 4, decade_filter = decade_filter))
    
@app.route('/add_track')
def add_track():
    """
    Takes the user to add-track.html allowing them to add a new track to the database
    """
    return render_template('add-track.html', genres=mongo.db.genres.find())
    
@app.route('/insert_track', methods=['POST']) # Because you're using POST here, you have to set that via methods
def insert_track():
    """
    This function gets the data the user inputs to the form on add-track.html and turns it into a new document in the database
    """
    # Format the timestamp that will be inserted into the record
    # The timestamp is a more user friendly version of the raw date object that is also created when a new document is created
    # The timestamp is what is displayed to the user, the raw date object is used in the backend, mainly for sorting
    
    # You can use jinja to do this
    timestamp = datetime.now().strftime('%d %B %Y %H:%M')
    # Get the tracks collection
    tracks = mongo.db.tracks
    # Insert the record using the fields from the form on add-track.html
    tracks.insert_one(
        {
            'track_title': request.form.get('track_title'), # Access the tasks collection
            'artist': request.form.get('artist'),
            'youtube_link': request.form.get('youtube_link'),
            'year': int(request.form.get('year')),
            'genre': request.form.get('genre'),
            'user_name': request.form.get('user_name'),
            'description': request.form.get('description'),
            # Upvotes is set to 1 by default. This idea is borrowed from Reddit, in that a user who uploads a track would presumably want to upvote it as well
            'upvotes': 1,
            # date_added is the human friendly date
            'date_added': timestamp,
            # date_added_raw is the python friendly date
            'date_added_raw': datetime.now()
        }
    )
    # Once submitted, redirect to the get_tracks function to view the collection using the default sorting order
    return redirect(url_for('get_tracks', sorting_order = 1, decade_filter = 'all'))
    
@app.route('/add_genre')
def add_genre():
    """
    Takes the user to add-genre.html, allowing them to add a new genre to the genre collection
    """
    return render_template('add-genre.html')
    
@app.route('/insert_genre', methods=['POST']) # Because you're using POST here, you have to set that via methods
def insert_genre():
    genres = mongo.db.genres
    genres.insert_one(
        {
            'genre': request.form.get('genre')    
        }
    )
    # There are 2 places the user can be adding a genre from; adding a new track or editing an existing track
    # If the genre_edit_track_id is not in session, that means the user is adding a new track
    if 'genre_edit_track_id' not in session:
        # In which case, just take them back to add-track.html to allow them to continue adding a track
        return redirect(url_for('add_track'))
    # Else the user is currently editing a track
    else: 
        # Take them back to edit-track.html, to the track they were editing before they went to adding a new genre
        # Pass through the session variables that were established by edit_track()
        return redirect(url_for('edit_track', decade_filter = session['decade_filter'], track_id = session['genre_edit_track_id'], sorting_order = session['sorting_order']))
    
@app.route('/upvote_track/<decade_filter>/<sorting_order>/<track_id>', methods=['POST'])
def upvote_track(decade_filter, sorting_order, track_id):
    tracks = mongo.db.tracks
    tracks.update( 
        {'_id': ObjectId(track_id)},
        # Increment the value of the upvote key by 1
        {'$inc': { 'upvotes': 1 }}
    )
    
    session['hold_pagination'] = True
    
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
    
@app.route('/edit_track/<decade_filter>/<sorting_order>/<track_id>')
# This function essential gets the task that matches this task id
def edit_track(sorting_order, decade_filter, track_id):
    # If genre_edit_track_id is in session, that means the user is coming from just adding a genre
    if 'genre_edit_track_id' in session:
        # Get the track_id from the session
        track_id = session['genre_edit_track_id']
        # Find the track the user wants to edit
        # Wrap track_id in ObjectId in order to make it acceptabke to mongodb
        the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
        # Pop the session since it's no longer needed
        session.pop('genre_edit_track_id', None)
    # If genre_edit_track_id is not in session, that means the user has not come from just adding a genre
    else:
        # Grab the track_id from what was passed through
        the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
    # A list of all the genres is also needed in order to populate the edit form
    all_genres = mongo.db.genres.find()
    
    # Hold pagination, once the user has finished editing they want go back to the 5 tracks they were viewing
    session['hold_pagination'] = True
    
    # Establish sessions for genre_edit in case the user ends up adding a new genre. Create variables that need to be passed back into edit_track once the user has finished adding a genre
    # Session variables are used here because add_genre can be called from both add_track and edit_track
    # If add_genre is called from add_track, default values for sorting_order and decade_filter can be hardcoded and they don't need to be passed through from anywhere
    # Hence, the session variables here are used as "standby" variables
    session['genre_edit_track_id'] = track_id
    session['sorting_order'] = sorting_order
    session['decade_filter'] = decade_filter
    # Render edit_track.html, pass through necessary variables
    return render_template('edit-track.html', decade_filter = decade_filter, sorting_order = sorting_order, track = the_track, genres = all_genres)
    
@app.route('/insert_edited_track/<decade_filter>/<sorting_order>/<track_id>', methods=["POST"])
def insert_edited_track(decade_filter, sorting_order, track_id):
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
        'year': int(request.form.get('year')),
        'genre':request.form.get('genre'),
        # These last three are the same values as what were created when the track was added to the database initially
        'upvotes': upvotes,
        'date_added': date_added,
        'date_added_raw': date_added_raw
    })
    
    # Pop the genre_edit_track_id session, the user won't need it again unless they come to editing a track again
    session.pop('genre_edit_track_id', None)
    
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
    
@app.route('/delete_track/<decade_filter>/<sorting_order>/<track_id>')
def delete_track(decade_filter, sorting_order, track_id):
    # Use ObjectId to parse the task_id in a format acceptable to mongo
    mongo.db.tracks.remove({'_id': ObjectId(track_id)})
    session['hold_pagination'] = True
    # Then go to the get_tasks function
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)