from flask import Flask, redirect, url_for, render_template, request
from cs50 import SQL
import time

app = Flask(__name__)

db = SQL('sqlite:///database.db')

@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=='GET'):
        return render_template('index.html')

    if(request.method=='POST'):
        hashed_url =  str( hash( time.time() ))

        URL = request.form['url']

        var = db.execute("SELECT TIMESTAMP FROM urls WHERE URL=:u",u=str(URL))

        if(len(var)<1):
            db.execute('INSERT INTO urls VALUES (:u,:t)',u= str( URL ) ,t=str(hashed_url) )
            return "Your shortened URL is: <a href = 'http://localhost:5000/" + hashed_url + "'> http://localhost:5000/" + hashed_url + "</a>"
        else:
            return "Your shortened URL is: <a href = 'http://localhost:5000/" + var[0]['TIMESTAMP'] + "'> http://localhost:5000/" + var[0]['TIMESTAMP'] + "</a>"


@app.route('/<url>')
def reach(url):
    value = db.execute("SELECT URL FROM urls WHERE TIMESTAMP=:u",u=str(url))
    return redirect(value[0]['URL'])

if(__name__=='__main__'):
    app.run(debug=True)
