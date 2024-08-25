from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Integer, nullable=False)
    minutes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<UserPreferences {self.phone}>'
