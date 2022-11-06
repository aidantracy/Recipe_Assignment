
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_app import app
from flask import render_template, redirect, flash, session, request

@app.route('/new_recipe')
def new_recipe():

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('new_recipe.html')

@app.route('/submit_recipe', methods=['POST'])
def create_recipe():

    # check to see if all fields were submitted 
    valid = Recipe.validate_recipe(request.form)
    if not valid:
        return redirect('/new_recipe')
    
    data = {
        'user_id' : session['user_id'],
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty']
    }

    Recipe.save_recipe(data)
    return redirect('/welcome')