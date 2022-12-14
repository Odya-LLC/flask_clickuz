# Flask-ClickUz
> Only for Uzbekistan


Click.uz integration for Flask

## Links
* [About ClickUz](https://click.uz/)
* [ClickUz Docs](https://docs.click.uz/)

## How it Works

### Install

```
pip install Flask-ClickUz
```

### Add your credentials from ClickUz to config file

```python
CLICK_SECRET = 'Your secret key'
CLICK_SERVICE_ID = 'Your service ID'
CLICK_MERCHANT_ID = "123" 
```

### Create Flask App With Flask-ClickUz

```python
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
    
    # Generate url for new orders
    url = click.Generate_Transaction(order_id=123, amount=50000, return_url = '/return_url')
    
    return app
```

### Flask-ClickUz models schema

```python
"""
Flask-ClickUz uses Flask-SQLAlchemy models to save data in database, it prefers to use Postgresql
"""
class Click_Transaction(db.Model):
    __tablename__ = 'click_transaction'
    id = db.Column(db.Integer, primary_key=True)
    click_trans_id = db.Column(db.Integer, unique=True)
    service_id = db.Column(db.Integer)
    click_paydoc_id = db.Column(db.Integer)
    merchant_trans_id = db.Column(db.String(255))
    amount = db.Column(db.Float)
    action = db.Column(db.Integer)
    error = db.Column(db.Integer)
    error_note = db.Column(db.String(255))
    sign_time = db.Column(db.DateTime)
    sign_string = db.Column(db.String(255))
```

### Accessing Models
Select data from models

```python
click.model # Click_Transaction 
Click_Transaction = click.model
transaction = Click_Transaction.query.all() # You can select or filter data
```

Add model view to Flask-Admin

```python
from flask_admin.contrib.sqla import ModelView
admin.add_view(ModelView(click.model, db.session))
```



## Task List

### SHOP-API methods

- [x] Prepare
- [x] Complete


### Merchant API methods

- [ ] create_invoice
- [ ] check_invoice
- [ ] create_card_token
- [ ] verify_card_token
- [ ] payment_with_card_token
- [ ] delete_card_token
- [ ] check_payment
- [ ] merchant_trans_id
- [ ] cancel




## Licence
This project is licensed under the MIT License (see the `LICENSE` file for details).