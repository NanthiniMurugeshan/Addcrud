from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mymongodb    #Select the database
todos = db.todo #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all Users
	data = todos.find()
	return render_template('index.html',datas=data)

@app.route("/")
def deful ():
	data = todos.find()
	return render_template('index.html', datas=data)
	
@app.route("/action", methods=['POST'])
def action ():
	#Adding a User
	data=request.form.to_dict()
	todos.insert(data)
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a User with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	data=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',datas=data)

@app.route("/updatedata", methods=['POST'])
def action3 ():
	#Updating a User with various references
	id = request.values.get("_id")
	data = request.form.to_dict()
	del data['_id']
	todos.update({"_id":ObjectId(id)}, {'$set':data})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a User with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
