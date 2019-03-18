import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'level-up'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds127115.mlab.com:27115/level-up'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tracks')
def get_tracks():
    return render_template("tracks.html",
    tracks=mongo.db.tracks.find())
    
@app.route('/add_track')
def add_track():
    return render_template('add-track.html') 
    
@app.route('/insert_track', methods=['POST']) # Because you're using POST here, you have to set that via methods
def insert_track():
    tracks = mongo.db.tracks # Get the tracks collection
    tracks.insert_one(request.form.to_dict()) # Whenever you submit something, it is submitted as a request object. We need to convert to a dictionary so that it can be understood by mongo
    return redirect(url_for('get_tracks')) # Once submitted, we redirect to the get_tasks function so that we can view our collection
    
@app.route('/upvote_track/<track_id>', methods=['POST'])
def upvote_track(track_id):
    tracks = mongo.db.tracks
    tracks.update( 
        {'_id': ObjectId(track_id)},
        {'$inc': { 'upvotes': 1 }}
    )
    
#     db.products.update(
#   { sku: "abc123" },
#   { $inc: { quantity: -2, "metrics.orders": 1 } }
#     )


    return redirect(url_for('get_tracks'))
 
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)