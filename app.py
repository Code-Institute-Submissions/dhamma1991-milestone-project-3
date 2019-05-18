# Use operating system dependant functionality
import os
# Allow full utilisation of Flask framework
from flask import Flask, render_template, redirect, request, url_for, session, flash
# Allow database manipulation
from flask_pymongo import PyMongo, pymongo
# Allow working with _id fields
from bson.objectid import ObjectId
# Allow date and time manipulation
from datetime import datetime, timedelta
# For database querying
from bson.son import SON

# Initialise Flask
app = Flask(__name__)
# Connect to Database
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

# Secret Key
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Initialise PyMongo
mongo = PyMongo(app)

""" INDEX PAGE """
@app.route('/index')
@app.route('/')
def index():
    print(os.urandom(20))
    """
    This is the default route
    Render the home page
    Grab the current top 3 tracks by upvotes and display them on the home page
    """
    
    # Clear any session variables the user may have 
    # This ensures the user can go to get_tracks cleanly
    session.clear()
    
    # Get the tracks collection
    tracks = mongo.db.tracks.find()
    
    # Set the html title
    title = "DesertIsland | Home"
    
    # Render the template, pass through necessary values
    return render_template("index.html", 
                            # Sort all tracks by upvotes descending, limit to 3 results
                            tracks = tracks.sort('upvotes', pymongo.DESCENDING).limit(3),
                            title = title
                            )
""" /INDEX PAGE """

""" ABOUT PAGE """
@app.route('/about')
def about():
    """
    Render the About page
    """
    
    # Set the html title
    title = "DesertIsland | About"
    
    # Render the template, pass through necessary values
    return render_template("about.html", title = title)
""" /ABOUT PAGE """

""" DATABASE STATS PAGE """
@app.route('/stats')
def stats():
    """
    Returns the stats template, populated with statistical values for the current database
    """
    
    # Get the tracks collection
    tracks_collection = mongo.db.tracks
    
    """ Total Number Of Tracks """
    # Count the number of tracks in the collection
    tracks_count = tracks_collection.count()
    """ /Total Number Of Tracks """
    
    """ Most Popular Decade By Number Of Tracks """
    # Find the decade with the most number of tracks
    # First, create a dictionary containing the counts of the number of tracks in each decade
    decades_dict = { 
        'Pre 1950s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1000}}, 
                                {"year": {'$lt': 1950}}
                                ]
                        }).count(),
        'The 1950s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1950}}, 
                                {"year": {'$lt': 1960}}
                                ]
                        }).count(),
        'The 1960s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1960}}, 
                                {"year": {'$lt': 1970}}
                                ]
                        }).count(),
        'The 1970s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1970}}, 
                                {"year": {'$lt': 1980}}
                                ]
                        }).count(),
        'The 1980s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1980}}, 
                                {"year": {'$lt': 1990}}
                                ]
                        }).count(),
        'The 1990s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 1990}}, 
                                {"year": {'$lt': 2000}}
                                ]
                        }).count(),
        'The 2000s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 2000}}, 
                                {"year": {'$lt': 2010}}
                                ]
                        }).count(),
        'The 2010s': tracks_collection.find({"$and": [
                                {"year": {'$gte': 2010}}, 
                                {"year": {'$lt': 2020}}
                                ]
                        }).count()
    }

    # Then get the max count, find the decade with the most tracks
    most_pop_decade = max(decades_dict, key=decades_dict.get)
    """ /Most Popular Decade By Number Of Tracks """
    
    """ Most Frequent """
    def most_freq(key_name):
        """
        Function that can be used to find the most frequent values for a given key in the database
        """
        # Establish a pipeline
        most_freq_pipeline = [
            # Sum the counts of each key name
            {"$group": {"_id": key_name, "count": {"$sum": 1}}},
            # Sort descending so highest is first
            {"$sort": SON([("count", -1)])}
        ]
            
        # Convert the results of the pipeline into a list, extract the first value (the highest count)
        most_freq_list = list(tracks_collection.aggregate(most_freq_pipeline))[0]
        
        # Get the value from the resultant dictionary
        return most_freq_list['_id']
        
    # Call most_freq for artist
    most_freq_artist = most_freq('$artist')
    # And user_name
    most_freq_user = most_freq('$user_name')
    # And genre
    most_freq_genre = most_freq('$genre')
    """ /Most Frequent """
    
    """ Sum Of Upvotes For All Tracks """
    # First, get a list of all the upvote values
    all_upvotes_list = list(tracks_collection.find( { },
                                    { 'upvotes': 1, '_id' :0 }
                                ))
    
    # Iterate through the list and sum the values
    all_upvotes = sum(item['upvotes'] for item in all_upvotes_list)
    """ /Sum Of Upvotes For All Tracks """
    
    """ Most Popular Artist By Likes """
    # Get a list of all the artists
    most_pop_artist = list(tracks_collection.aggregate([
        # Group by artist
         { '$group': { '_id': "$artist", 
             # Sum the upvotes for each artist
             'upvotes': { '$sum': '$upvotes' } } },
        # Sort descending
         { '$sort': { 'upvotes': -1 } }]))[0] # Grab the first item (the highest)
    """ /Most Popular Artist By Likes """

    # Set the html title
    title = "DesertIsland | Stats"
    
    # Render the template, pass through necessary values
    return render_template("stats.html", 
        title = title, 
        tracks_count = tracks_count, 
        most_pop_decade = most_pop_decade, 
        most_freq_artist = most_freq_artist,
        most_freq_user = most_freq_user,
        most_freq_genre = most_freq_genre,
        all_upvotes = all_upvotes,
        most_pop_artist = most_pop_artist)
""" /DATABASE STATS """

""" GET_TRACKS """
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
    # (e.g. they've clicked 'Next' in the list of tracks)
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
    
    # # Pop the genre_edit_track_id session
    # # This stops the same track id from getting passed through to edit no matter which track the user chooses to edit
    # session.pop('genre_edit_track_id', None)
    
    # Determine the tracks to return based on the decade filter, the value of which is determined by the select box on tracks.html
    if decade_filter == "pre1950":
        tracks_decade = tracks_collection.find({"$and": [
                                {"year": {'$gte': 1000}}, 
                                {"year": {'$lt': 1950}}
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
    # Also determines whether to show a message if no tracks have been found for a particular filter
    tracks_count = tracks.count() 
    
    # Set the html title
    title = "DesertIsland | Charts"

    # Render tracks.html
    # tracks is the list of tracks to be rendered
    # sorting_order is how they are to be sorted (corresponding to the system in the if/else statement above)
    # pagination determines how many tracks are to be skipped. The user navigates through the pagination using the next and previous buttons on tracks.html
    # tracks_col_count determines whether to hide the next and previous buttons. If the user has reached the end of the list it doesn't make sense and would be confusing for them to be able to click 'Next'
    # title is the html title
    return render_template("tracks.html", 
        tracks = tracks,
        decade_filter = decade_filter,
        sorting_order = sorting_order,
        pagination = pagination,
        tracks_count = tracks_count,
        title = title
        )
""" /GET_TRACKS """                    

""" NEXT TRACKS """
@app.route('/next_tracks/<decade_filter>/<int:sorting_order>')
def next_tracks(decade_filter, sorting_order):
    """
    This function takes the user to the next 5 tracks, determined by the pagination the user is currently on, the sorting order they are currently using as well as the filtering options set
    """
    
    # Set pagination. If the user clicks 'next', pagination is increased by 5
    session['pagination'] += 5
    session['hold_pagination'] = True
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
""" /NEXT TRACKS """         

""" PREV TRACKS """
@app.route('/prev_tracks/<decade_filter>/<int:sorting_order>')
def prev_tracks(decade_filter, sorting_order):
    """
    This function takes the user to the previous 5 tracks, determined by the pagination the user is currently on, the sorting order they are currently using as well as the filtering options set
    """
    
    # Set pagination. If the user clicks 'previous', pagination is decreased by 5
    session['pagination'] -= 5
    session['hold_pagination'] = True
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
""" /PREV TRACKS """

""" SORT TRACKS UPVOTES DESC """
@app.route('/sort_tracks_upvote_desc/<decade_filter>')
def sort_tracks_upvote_desc(decade_filter):
    """
    Change the sorting order to show tracks with HIGHEST upvotes first. This is the default sorting order
    """
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', sorting_order = 1, decade_filter = decade_filter))
""" /SORT TRACKS UPVOTES DESC """

""" SORT TRACKS UPVOTES ASC """
@app.route('/sort_tracks_upvote_asc/<decade_filter>')
def sort_tracks_upvote_asc(decade_filter):
    """
    Change the sorting order to show tracks with LOWEST upvotes first
    """
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', sorting_order = 2, decade_filter = decade_filter))
""" /SORT TRACKS UPVOTES ASC """
    
""" SORT TRACKS DATE_ADDED DESC """
@app.route('/sort_tracks_date_added_desc/<decade_filter>')
def sort_tracks_date_added_desc(decade_filter):
    """
    Change the sorting order to show NEWEST tracks by date added first
    """
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', sorting_order = 3, decade_filter = decade_filter))
""" /SORT TRACKS DATE_ADDED DESC """
  
""" SORT TRACKS DATE_ADDED ASC """  
@app.route('/sort_tracks_date_added_asc/<decade_filter>')
def sort_tracks_date_added_asc(decade_filter):
    """
    Change the sorting order to show OLDEST tracks by date added first
    """
    
    # Render the template, pass through necessary values
    return redirect(url_for('get_tracks', sorting_order = 4, decade_filter = decade_filter))
""" /SORT TRACKS DATE_ADDED ASC """
    
""" TRACK DETAIL PAGE """
@app.route('/track_detail/<decade_filter>/<sorting_order>/<track_id>')
def track_detail(decade_filter, sorting_order, track_id):
    """
    Render the detailed view for each track, displaying all database fields
    """
    
    # Grab the track_id from what was passed through
    the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
    
    # Format the page title
    title = "DesertIsland | " + the_track.get("artist") + " - " + the_track.get('track_title')
    
    # Render the template, pass through necessary values
    return render_template("track-detail.html", title = title, decade_filter = decade_filter, sorting_order = sorting_order, track = the_track)
""" /TRACK DETAIL PAGE """
    
""" ADD TRACK PAGE """
# If the user inserts a new genre from the add_track page, ensure the newly inserted genre gets set as the value for the genre dropdown box
# To do this, it gets passed through from insert_genre
# By default, the user hasn't inserted a new genre
@app.route('/add_track', defaults={'inserted_genre': None})
@app.route('/add_track/<inserted_genre>')
def add_track(inserted_genre):
    """
    Takes the user to add-track.html allowing them to add a new track to the database
    """
    
    # Render the template, pass through necessary values
    return render_template('add-track.html', 
        genres=mongo.db.genres.find(),
        inserted_genre = inserted_genre)
""" /ADD TRACK PAGE """
    
""" INSERT TRACK """
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
    
    # Feedback to the user the track was successfully submitted
    flash('Track added successfully!')
    
    # Once submitted, redirect to the get_tracks function to view the collection using the default sorting order
    return redirect(url_for('get_tracks', 
        sorting_order = 1, 
        decade_filter = 'all'))
""" /INSERT TRACK """ 

""" ADD GENRE PAGE """
# add_genre might not always need a track_id; track_id is only needed if the user is coming to add_genre from editing a track
@app.route('/add_genre', defaults={'track_id': None})
@app.route('/add_genre/<track_id>')
def add_genre(track_id):
    """
    Takes the user to add-genre.html, allowing them to add a new genre to the genre collection
    """
    
    # Set the html title
    title = "DesertIsland | Add A New Genre"
    
    # Render the template
    return render_template('add-genre.html', 
        track_id = track_id,
        title = title)
""" /ADD GENRE PAGE """

""" CANCEL ADD GENRE """
# Pass through track_id if needed, this is so the user goes back to the same track they were editing
@app.route('/cancel_add_genre', defaults={'track_id': None})
@app.route('/cancel_add_genre/<track_id>')
def cancel_add_genre(track_id):
    """
    Cancels adding a genre, adding nothing to the database
    Take the user back to either add_track or depending on where they were before going to add_genre
    """
    
    # If track_id exists this means the user was editing a track
    if track_id:
        # Take them back to the track they were editing, pass through the required session variables 
        return redirect(url_for('edit_track', track_id = track_id, decade_filter = session['decade_filter'], sorting_order = session['sorting_order']))
    # If track_id doesn't exist, the user must be adding a new track
    else:
        # Take them back to add_track
        return redirect(url_for('add_track'))
""" /CANCEL ADD GENRE """
 
""" INSERT GENRE """
# If track_id hasn't been passed through, set a default of None
@app.route('/insert_genre', defaults={'track_id': None}, methods=['POST'])   
@app.route('/insert_genre/<track_id>', methods=['POST'])
def insert_genre(track_id):
    """
    Insert a new genre into the database
    """
    
    genres = mongo.db.genres
    
    inserted_genre = request.form.get('genre')
    
    genres.insert_one(
        {
            'genre': inserted_genre
        }
    )
    
    # Feedback to the user the genre was successfully submitted
    flash('Genre added successfully!')
    
    # There are 2 places the user can be adding a genre from; adding a new track or editing an existing track
    # If track_id has a value, that means the user is editing a track
    if track_id:
        # Take them back to edit-track.html, to the track they were editing before they went to adding a new genre
        # Pass through the session variables that were established by edit_track()
        return redirect(url_for('edit_track', 
            track_id = track_id, 
            decade_filter = session['decade_filter'], 
            sorting_order = session['sorting_order'],
            inserted_genre = inserted_genre))
            
    # Else the user is currently adding a new track
    else: 
        # In which case, just take them back to add-track.html to allow them to continue adding a track
        return redirect(url_for('add_track',
            inserted_genre = inserted_genre))
""" /INSERT GENRE """

""" UPVOTE TRACK """
# Tracks can be upvoted from both the charts page and the track-detail page
# This first route is for a charts page upvote
@app.route('/upvote_track/<decade_filter>/<sorting_order>/<track_id>', defaults={'track_detail': False}, methods=['POST'])
# Second route is for a track-detail upvote
@app.route('/upvote_track/<decade_filter>/<sorting_order>/<track_id>/<track_detail>', methods=['POST'])
def upvote_track(decade_filter, sorting_order, track_id, track_detail):
    """ 
    Allows the user to upvote a track and saves the new upvote value
    """
    
    tracks = mongo.db.tracks # Get the tracks collection
    
    tracks.update(  #  Update the collection
        {'_id': ObjectId(track_id)},
        # Increment the value of the upvote key by 1
        {'$inc': { 'upvotes': 1 }}
    )
    
    # Hold pagination, for if a user is upvoting from the charts page
    session['hold_pagination'] = True
    
    # If the user is upvoting from a track_detail page
    if track_detail:
        # Ensure the user stays on the same track-detail page
        return redirect(url_for('track_detail', decade_filter = decade_filter, sorting_order = sorting_order, track_id = track_id))
        
    # Else the user is upvoting from the charts page
    else:
        # Render tracks.html, pass through necessary values to ensure the same decade_filter and sorting_order is set
        return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
""" /UPVOTE TRACK """

""" EDIT TRACK PAGE """
@app.route('/edit_track/<decade_filter>/<sorting_order>/<track_id>', defaults={'inserted_genre': None})
@app.route('/edit_track/<decade_filter>/<sorting_order>/<track_id>/<inserted_genre>')
def edit_track(sorting_order, decade_filter, track_id, inserted_genre):
    """
    Determines which track the user wants to edit
    Then takes them to edit-track.html
    """
    
    # If genre_edit_track_id is in session, that means the user is coming from just adding a genre
    # if 'genre_edit_track_id' in session:
    #     # Get the track_id from the session
    #     track_id = session['genre_edit_track_id']
    #     # Find the track the user wants to edit
    #     # Wrap track_id in ObjectId in order to make it acceptabke to mongodb
    #     the_track = mongo.db.tracks.find_one({"_id": ObjectId(track_id)})
    #     # Pop the session since it's no longer needed
    #     print(session['genre_edit_track_id'])
    #     session.pop('genre_edit_track_id', None)
    # If genre_edit_track_id is not in session, that means the user has not come from just adding a genre
    # else:
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
    session['sorting_order'] = sorting_order
    session['decade_filter'] = decade_filter
    # Render edit_track.html, pass through necessary variables
    return render_template('edit-track.html', 
    decade_filter = decade_filter, 
    sorting_order = sorting_order, 
    track = the_track, 
    genres = all_genres,
    inserted_genre = inserted_genre)
""" /EDIT TRACK """ 
    
""" INSERT EDITED TRACK """
@app.route('/insert_edited_track/<decade_filter>/<sorting_order>/<track_id>', methods=["POST"])
def insert_edited_track(decade_filter, sorting_order, track_id):
    """
    Takes the data the user fills out within the form in edit-track.html
    and saves the updated item to the database
    """
    
    # Get the tracks collection
    tracks = mongo.db.tracks
    
    # In order for the edit to work properly, some values that the user should not be eligible to update (e.g. upvotes) need to be retrieved from the the database prior to update
    # If not, update will delete any old key/values that aren't explicitly passed through with the update
    # In order to do this, find() is used to grab a cursor of the track being edited
    old_values = tracks.find({"_id": ObjectId(track_id)})
    
    # Loop through the cursor and get the values the user shouldn't be able to change
    # Once tracks.update occurs, any values not specified within the update won't be added to the database
    # That would mean the track would lose its upvotes, date_added, date_added_raw and user_name
    for item in old_values:
        upvotes = item['upvotes']
        date_added = item['date_added']
        date_added_raw = item['date_added_raw']
        user_name = item['user_name']
    
    # Do the update
    tracks.update( {'_id': ObjectId(track_id)},
    {
        'track_title': request.form.get('track_title'),
        'artist': request.form.get('artist'),
        'youtube_link': request.form.get('youtube_link'),
        'year': int(request.form.get('year')),
        'genre': request.form.get('genre'),
        'description': request.form.get('description'),
        # These last four are the same values as what were created when the track was added to the database initially
        # Editing a user name is not an option. It's not desirable for users to steal someone's track upload!
        'user_name': user_name,
        'upvotes': upvotes,
        'date_added': date_added,
        'date_added_raw': date_added_raw
    })
    
    # Pop the genre_edit_track_id session, the user won't need it again unless they come to editing a track again
    session.pop('genre_edit_track_id', None)
    
    # Go back to get_tracks
    return redirect(url_for('get_tracks', 
        decade_filter = decade_filter, 
        sorting_order = sorting_order))
""" /INSERT EDITED TRACK """    
    
""" DELETE TRACK """
@app.route('/delete_track/<decade_filter>/<sorting_order>/<track_id>')
def delete_track(decade_filter, sorting_order, track_id):
    """
    Deletes a track from the database
    """
    
    # Use ObjectId to parse the track_id in a format acceptable to mongo
    mongo.db.tracks.remove({'_id': ObjectId(track_id)})
    
    # Hold pagination so the user is taken back to the same tracks they were viewing (minus the one they just deleted)
    session['hold_pagination'] = True
    
    # Return the updated list of tracks
    return redirect(url_for('get_tracks', decade_filter = decade_filter, sorting_order = sorting_order))
""" /DELETE TRACK """

""" INITIALISE APP """
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
""" /INITIALISE APP """