import db

def get_user(user_id):
	sql = """SELECT id, username
			 FROM users
			 WHERE id = ?"""
	result = db.query(sql, [user_id])
	return result[0] if result else None

def get_recipes(user_id):
	sql = "SELECT id, title FROM recipes WHERE user_id = ? ORDER BY title"
	return db.query(sql, [user_id])