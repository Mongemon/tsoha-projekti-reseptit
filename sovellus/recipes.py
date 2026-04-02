import db

def get_all_classes():
	sql = "SELECT title, value FROM classes ORDER BY id"
	result = db.query(sql)

	classes = {}
	for title, value in result:
		classes[title] = []
	for title, value in result:
		classes[title].append(value)
	return classes

def add_recipe(title, description, ingredients, instructions, user_id, classes):
	sql = """INSERT INTO recipes (title, description, ingredients, instructions,
        user_id) VALUES (?, ?, ?, ?, ?)"""
	db.execute(sql, [title, description, ingredients, instructions, user_id])

	recipe_id = db.last_insert_id()

	sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
	for title, value in classes:
		db.execute(sql, [recipe_id, title, value])

def get_classes(recipe_id):
	sql = "SELECT title, value FROM recipe_classes WHERE recipe_id =?"
	return db.query(sql, [recipe_id])

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
	result = db.query(sql, [recipe_id])
	return result[0] if result else None

def update_recipe(recipe_id, title, description, ingredients, instructions, classes):
	sql = """UPDATE recipes SET title = ?,
							  description = ?,
							  ingredients = ?,
							  instructions = ?
							Where id = ?"""
	db.execute(sql, [title, description, ingredients, instructions, recipe_id])

	sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
	db.execute(sql, [recipe_id])

	sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
	for title, value in classes:
		db.execute(sql, [recipe_id, title, value])

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
