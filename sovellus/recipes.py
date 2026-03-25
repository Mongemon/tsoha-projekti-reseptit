import db

def add_recipe(title, description, ingredients, instructions, user_id):
	sql = """INSERT INTO recipes (title, description, ingredients, instructions,
        user_id) VALUES (?, ?, ?, ?, ?)"""
	db.execute(sql, [title, description, ingredients, instructions, user_id])

def get_recipes():
	sql = """SELECT id, title FROM recipes ORDER BY title"""
	return db.query(sql)

def get_recipe(recipe_id):
	sql = """SELECT recipes.title,
					recipes.description,
					recipes.ingredients,
					recipes.instructions,
					users.username
			  FROM recipes, users
			  Where recipes.user_id = users.id AND
					recipes.id = ?"""
	return db.query(sql, [recipe_id])[0]