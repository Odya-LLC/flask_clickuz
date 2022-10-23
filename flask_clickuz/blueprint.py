from flask import Blueprint, jsonify, request
import hashlib, datetime


def check_in_req(data):
    return 'click_trans_id' in data\
        and 'service_id' in data\
        and 'click_paydoc_id' in data\
        and 'merchant_trans_id' in data\
        and 'amount' in data\
        and 'action' in data\
        and 'error' in data\
        and 'error_note' in data\
        and 'sign_time' in data\
        and 'sign_string' in data

def check_hash_code(data,secret_key):
    s = f"{data['click_trans_id']}{data['service_id']}{secret_key}{data['merchant_trans_id']}{data['amount']}{data['action']}{data['sign_time']}"
    s = hashlib.md5(s.encode('utf-8')).hexdigest()
    return s == data['sign_string']

def Create_Blueprint(click):
    bp = Blueprint('click', __name__, url_prefix='/click')
    
    @bp.route('/prepare', methods=['POST'])
    def prepare():
        print(request.form)
        """md5( click_trans_id + 
        service_id +
        SECRET_KEY* +
        merchant_trans_id +
        amount +
        action + 
        sign_time)        """
        data = dict(request.form)
        if not check_in_req(data):
            return jsonify({"status" : "error"}), 400
        
        model = click.model
        new_transaction = model(
            click_trans_id = data.get('click_trans_id'),
            service_id = data.get('service_id'),
            click_paydoc_id = data.get('click_paydoc_id'),
            merchant_trans_id = data.get('merchant_trans_id'),
            amount = data.get('amount'),
            action = data.get('action'),
            error = data.get('error'),
            error_note = data.get('error_note'),
            sign_time = datetime.datetime.strptime(data.get('sign_time'), '%Y-%m-%d %H:%M:%S'),
            sign_string = data.get('sign_string')
        )
        click.db.session.add(new_transaction)
        click.db.session.commit()
        
        if not check_hash_code(data, click.click_secret):
            new_transaction.error = '-1'
            new_transaction.error_note = click.errors.get_error('-1')
            click.db.session.commit()
            res = new_transaction.response()
            click.db.session.delete(new_transaction)
            click.db.session.commit()
            return jsonify(res), 200
        
        
        
        return jsonify(new_transaction.response()), 200
    
    @bp.route('/complete', methods=['POST'])
    def complete():
        return jsonify({"status": "ok"})
    return bp


