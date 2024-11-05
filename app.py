from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "secretkey"  # Needed for flash messages and session handling

# Mock database for storing user data (use a real database for production)
user_database = {}

@app.route("/")
def home():
    # Check if the user is logged in
    if "username" in session:
        return render_template("index.html")  # Show chocolate shop page if logged in
    else:
        flash("Please log in to access the Chocolate Shop.")
        return redirect(url_for("login"))  # Redirect to login page if not logged in

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in user_database and user_database[username] == password:
            session["username"] = username  # Store username in session
            flash("Login successful!")
            return redirect(url_for("home"))  # Redirect to the home page
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in user_database:
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("register"))
        user_database[username] = password
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)  # Remove the username from session
    flash("You have been logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
