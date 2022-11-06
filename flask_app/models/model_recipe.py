from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_user import User
from flask import flash

db = 'recipes'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.under_thirty = data['under_thirty']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.author = None

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        print('DATA***', data)
        if ((len(data['recipe_name']) < 3) or (len(data['description']) < 3) or (len(data['instructions']) < 3)):
            flash('Name, Description, and Instructions need to be at least 3 letters', 'new_recipe')
            is_valid = False
        if not data['date_made']:
            flash('Select date made', 'new_recipe')
            is_valid = False
        if not data['under_thirty']:
            flash('Select yes or no')
        
        return is_valid
    
    # create recipe
    @classmethod
    def save_recipe(cls, data):

        query = """
                INSERT INTO recipes(user_id, recipe_name, under_thirty, description, instructions, date_made)
                VALUES(%(user_id)s, %(recipe_name)s, %(under_thirty)s, %(description)s, %(instructions)s, %(date_made)s)
                """
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_all_recipes(cls):

        query = """
                SELECT * FROM users 
                JOIN recipes ON users.id = recipes.user_id
                """
        results = connectToMySQL(db).query_db(query)

        all_recipes = []
        for row in results:
            recipe = cls(row)

            recipe_author_info = {
                'id' : row['user_id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }

            author = User(recipe_author_info)
            recipe.author = author
            all_recipes.append(recipe)
        
        return all_recipes




