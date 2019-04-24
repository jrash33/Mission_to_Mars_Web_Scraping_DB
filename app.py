# import necessary libraries
from flask import Flask, render_template, redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
#import scrape function created to get mars info from web
from scrape_mars import scrape

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
#db.team.drop()

# create mongo connection
collection = db.mars_data

# create route that renders index.html template
@app.route("/")
def mars_data():
    mars_final_data = db.collection.find_one()
    return render_template("index.html", mars_data=mars_final_data)

@app.route("/scrape")
def scraper():
    mars_final_data = scrape()
    db.collection.update({}, mars_final_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)