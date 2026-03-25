import db

def add_recipe(title, description, ingredients, instructions, user_id):
	sql = """INSERT INTO recipes (title, description, ingredients, instructions,
        user_id) VALUES (?, ?, ?, ?, ?)"""
	db.execute(sql, [title, description, ingredients, instructions, user_id])

