from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt

@app.route('/new')
def create_planet_form():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new.html')

@app.route('/back')
def back():
    return redirect('/dashboard')


@app.route('/submit/tv', methods=["POST"])
def submit_show():
    if "user_id" not in session:
        return redirect('/')
    #validations
    if not Show.validate_new(request.form):
        return redirect('/new')
    data = {
        "name" : request.form["name"],
        "network" : request.form["network"],
        "date" : request.form["date"],
        "description" : request.form["description"],
        "user_id" : session["user_id"]
    }
    Show.create(data)
    return redirect('/dashboard')

@app.route("/tv/edit/<int:id>")
def show_edit_page(id):
    if "user_id" not in session:
        return redirect('/')
    data ={ 
        "id":id
    }
    return render_template("edit_tv.html",show=Show.get_one(data))

@app.route('/tv/update/<int:id>', methods = ["POST"])
def update(id):
    if "user_id" not in session:
        return redirect('/')
    if not Show.validate_new(request.form):
        return redirect('/new')
    data = {
        "id" : id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "network" : request.form['network'],
        "date" : request.form['date'],
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/tv/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    Show.delete(data)
    return redirect('/dashboard')


@app.route('/show/view/<int:show_id>')
def show_detail(show_id):
    if "user_id" not in session:
        return redirect('/')
    user = User.get_id(session["user_id"])
    show = Show.get_by_id(show_id)
    return render_template("view.html", user=user, show=show)