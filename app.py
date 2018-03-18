from flask import Flask, render_template #from flask, we want to import flask and render_template
from data import Reviews #from data.py, import the Reviews function

app = Flask(__name__) #creates an instance of flask

Reviews = Reviews()

@app.route('/') #points flask to the index so it can load files
def index():
    return render_template('index.html', reviews = Reviews) #literally just return a string

if __name__ == '__main__': #if the right application is being run...
    app.run(debug = True) #run it. debut means you don't have to reload the server for every change
