from extensions import db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency = db.Column(db.String(10), default="USD")  # Moeda preferida
    language = db.Column(db.String(10), default="en")  # Idioma preferido
    theme = db.Column(db.String(20), default="light")  # Tema do app

    user = db.relationship('User', backref=db.backref('settings', lazy=True, uselist=False))
