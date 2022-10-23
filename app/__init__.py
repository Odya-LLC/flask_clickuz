from flask import Flask
from flask_clickuz import Click
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

click = Click(db)


def Check_Allowment():
    return True

def Click_Callback(data):
    print(data)

def create_app():
    
    
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    click.Register_Callback(Click_Callback)
    click.Register_Validator(Check_Allowment)
    click.init_app(app)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
    
    return app