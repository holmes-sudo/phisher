from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<User {self.username}, Password {self.password}>"


class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    pin = db.Column(db.String(8), unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<Username: {self.username}, Password: {self.password}, Pin: {self.pin}>"
        )
