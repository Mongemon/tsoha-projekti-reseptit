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

	return recipe_id

def add_comment(recipe_id, user_id, comment, grade):
	sql = """INSERT INTO comments (recipe_id, user_id, comment)
			 VALUES (?, ?, ?)"""
	db.execute(sql, [recipe_id, user_id, comment])

	sql = "INSERT INTO grades (recipe_id, user_id, grade) VALUES (?, ?, ?)"
	db.execute(sql, [recipe_id, user_id, grade])

def get_classes(recipe_id):
	sql = "SELECT title, value FROM recipe_classes WHERE recipe_id =?"
	return db.query(sql, [recipe_id])

def get_recipeinfo():
	sql = """SELECT recipes.id, recipes.title, users.id user_id, users.username
			 FROM users, recipes 
			 WHERE recipes.user_id = users.id
			 ORDER BY recipes.title"""
	return db.query(sql)

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

def get_comments(recipe_id):
	sql = """SELECT comments.comment, users.id user_id, users.username
			 FROM comments, users
			 WHERE comments.recipe_id = ? AND comments.user_id = users.id
			 ORDER BY comments.id DESC"""
	return db.query(sql, [recipe_id])

def get_meangrade(recipe_id):
	sql = """SELECT AVG(grade)
			 FROM grades
			 WHERE recipe_id = ?"""
	result = db.query(sql, [recipe_id])
	return f"{result[0][0]:.1f}" if result and result[0][0] is not None else None

def has_commented(recipe_id, user_id):
	sql = """SELECT comment
			 FROM comments
			 WHERE recipe_id = ? AND user_id = ?
			 LIMIT 1"""
	result = db.query(sql, [recipe_id, user_id])
	return bool(result)

def get_images(recipe_id):
	sql = "SELECT id FROM images WHERE recipe_id = ?"
	return db.query(sql, [recipe_id])

def add_image(recipe_id, image):
	sql = "INSERT INTO images (recipe_id, image) VALUES (?, ?)"
	db.execute(sql, [recipe_id, image])

def get_image(image_id):
	sql = "SELECT image FROM images WHERE id = ?"
	result = db.query(sql, [image_id])
	return result[0][0] if result else None

def remove_image(recipe_id, image_id):
	sql = "DELETE FROM images WHERE id = ? AND recipe_id =?"
	db.execute(sql, [image_id, recipe_id])

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
	sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
	db.execute(sql, [recipe_id])

	sql = "DELETE FROM images WHERE recipe_id = ?"
	db.execute(sql, [recipe_id])

	sql = "DELETE FROM comments WHERE recipe_id = ?"
	db.execute(sql, [recipe_id])

	sql = "DELETE FROM grades WHERE recipe_id = ?"
	db.execute(sql, [recipe_id])

	sql = "DELETE FROM recipes WHERE id = ?"
	db.execute(sql, [recipe_id])

def find_recipe(query):
	sql = """SELECT id, title
			 FROM recipes
			 WHERE description LIKE ? OR title LIKE ?
			 ORDER BY title"""
	like = "%" + query + "%"
	return db.query(sql, [like, like])
