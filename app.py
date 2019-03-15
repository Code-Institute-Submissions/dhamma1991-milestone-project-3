import os
from flask import Flask
from flask_pymongo import pymongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'level-up'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds127115.mlab.com:27115/level-up'

@app.route('/')
def hello():
    return "Sup, name change successful, 2nd test change"
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)