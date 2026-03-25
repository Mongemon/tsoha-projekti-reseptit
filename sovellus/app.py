import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import config
import db
import recipes

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes = all_recipes)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    return render_template("show_recipe.html", recipe=recipe)

@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]

    recipes.add_recipe(title, description, ingredients, instructions, user_id)

    return redirect("/")

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    recipe_id = request.form["recipe_id"]
    title = request.form["title"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]

    recipes.update_recipe(recipe_id, title, description, ingredients, instructions)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    if request.method == "GET":
        recipe = recipes.get_recipe(recipe_id)
        return render_template("remove_recipe.html", recipe=recipe)
    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))



@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")