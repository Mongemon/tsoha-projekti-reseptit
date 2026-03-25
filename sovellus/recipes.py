import db

def add_recipe(title, description, ingredients, instructions, user_id):
	sql = """INSERT INTO recipes (title, description, ingredients, instructions,
        user_id) VALUES (?, ?, ?, ?, ?)"""
	db.execute(sql, [title, description, ingredients, instructions, user_id])

def get_recipes():
	sql = """SELECT id, title FROM recipes ORDER BY title"""
	return db.query(sql)

def get_recipe(recipe_id):
	sql = """SELECT recipes.id,
					recipes.title,
					recipes.description,
					recipes.ingredients,
					recipes.instructions,
					users.id user_id,
					users.username
			  FROM recipes, users
			  Where recipes.user_id = users.id AND
					recipes.id = ?"""
	return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, title, description, ingredients, instructions):
	sql = """UPDATE recipes SET title = ?,
							  description = ?,
							  ingredients = ?,
							  instructions = ?
							Where id = ?"""
	db.execute(sql, [title, description, ingredients, instructions, recipe_id])

def remove_recipe(recipe_id):
	sql = "DELETE FROM recipes WHERE id = ?"
	db.execute(sql, [recipe_id])

def find_recipe(query):
	sql = """SELECT id, title
			 FROM recipes
			 WHERE description LIKE ? OR title LIKE ?
			 ORDER BY title"""
	like = "%" + query + "%"
	return db.query(sql, [like, like])
