#Importing dependecies
# we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
#we'll use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#to use the scraping code, we will convert from Jupyter notebook to Python
import scraping

#Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#tell Python that our app will connect to Mongo using URI, uniform resource identifier
#"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
#This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


#Define the route for our HTML page
@app.route("/")
def index():
    #mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   #return render_template("index.html" tells Flask to return an HTML template using an index.html file.
   # mars=mars) tells Python to use the "mars" collection in MongoDB
   return render_template("index.html", mars=mars)


#Add next route,scrape
@app.route("/scrape")
def scrape():
    #we assign a new variable that points to our Mongo database: mars = mongo.db.mars.
   mars = mongo.db.mars
   # we created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). 
   # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
   

#run flask
if __name__ == "__main__":
   app.run()


