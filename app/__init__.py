from flask import Flask
from flask_clickuz import Click
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
click = Click(db)
orders = [525]

def Check_Allowment(data):
    """Calls when click sends request to server

    Args:
        data (dict): Click data, contains merchant_trans_id to check allownment

    Returns:
        Boolen: Return True if allownment is valid else False
    """    
    merchant_trans_id = data.get('merchant_trans_id')
    if int(merchant_trans_id) in orders:
        return True
    return False

def Click_Callback(transaction):
    """Calls when transaction is completed or cancelled, 
    if transaction is completed, transaction.action is 1
    else transaction.action is 0
    
    Args:
        transaction (Click_Transaction): SQLAlchemy model of Click_Transaction
    """   
    action = transaction.action # 0 - cancaled, 1 - paid
    pass

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    click.Register_Callback(Click_Callback) # Register callback
    click.Register_Validator(Check_Allowment) # Register validator
    click.init_app(app)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
    url = click.Generate_Transaction(order_id=123, amount=50000, return_url = '/return_url')
    print(url)
    return app