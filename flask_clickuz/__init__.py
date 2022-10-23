from flask import Flask, Blueprint
from .blueprint import Create_Blueprint
from .exceptions import Flask_ClickUz_Exception
from .errors import ClickUz_Errors
class Click:
    def __init__(self, db):
        self.validator = None
        self.db = db
        self.callback = None
        click_secret = None
        click_service_id = None
        click_merchant_id = None
        self.errors = ClickUz_Errors()
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
            
            
            def __repr__(self):
                return "%s"%(self.merchant_trans_id)
            
    
            def response(self):
                return {
                    "click_trans_id" : self.click_trans_id,
                    "merchant_trans_id" : self.merchant_trans_id,
                    "merchant_prepare_id" : self.id,
                    "error" : self.error,
                    "error_note" : self.error_note
                }
            def response_confirm(self):
                return {
                    "click_trans_id" : self.click_trans_id,
                    "merchant_trans_id" : self.merchant_trans_id,
                    "merchant_confirm_id" : self.id,
                    "error" : self.error,
                    "error_note" : self.error_note
                }
            
        self.model = Click_Transaction   
        
        pass
    def init_app(self, app: Flask):
        click_secret = app.config.get('CLICK_SECRET')
        click_service_id = app.config.get('CLICK_SERVICE_ID')
        click_merchant_id = app.config.get('CLICK_MERCHANT_ID')
        if not click_secret:
            raise Flask_ClickUz_Exception('CLICK_SECRET is not set')
        if not click_service_id:
            raise Flask_ClickUz_Exception('CLICK_SERVICE_ID is not set')
        if not click_merchant_id:
            raise Flask_ClickUz_Exception('CLICK_MERCHANT_ID is not set')
        if not self.validator:
            raise Flask_ClickUz_Exception('Validator is not set, Set validator with Register_Validator method')
        if not self.callback:
            raise Flask_ClickUz_Exception('Callback is not set, Set callback with Register_Callback method')
        self.click_secret = click_secret
        self.click_service_id = click_service_id
        self.click_merchant_id = click_merchant_id
        bp = Create_Blueprint(self)
        app.register_blueprint(bp)
        
    
    def Register_Validator(self, validator):
        """Calls when click sends request to server

        Args:
            validator (function): Callback function, it takes click data as argument
        """ 
        self.validator = validator
    
    def Register_Callback(self, callback):
        """Calls when transaction is completed or cancelled, 
        if transaction is completed, transaction.action is 1
        else transaction.action is 0
        
        Args:
            callback (Function): Register callback function, it takes transaction as argument
        """
        self.callback = callback
        
    def Generate_Transaction(self, order_id, amount, return_url=None):
        """_summary_

        Args:
            order_id (int): ID of order
            amount (int): amount of order to pay
            return_url (string, optional): Return url after payment. Defaults to None.

        Returns:
            string: Url for payment
        """        
        merchant_id = self.click_merchant_id
        service_id = self.click_service_id
        url = f"https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={amount}&transaction_param={order_id}"
        if return_url:
            url += f"&return_url={return_url}"
        return url
    