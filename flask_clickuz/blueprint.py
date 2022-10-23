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


def check_hash_code_prepare(data, secret_key, t_id):
    s = f"{data['click_trans_id']}{data['service_id']}{secret_key}{data['merchant_trans_id']}{t_id}{data['amount']}{data['action']}{data['sign_time']}"
    s = hashlib.md5(s.encode('utf-8')).hexdigest()
    return s == data['sign_string']


def Create_Blueprint(click):
    bp = Blueprint('click', __name__, url_prefix='/click')
    
    @bp.route('/prepare', methods=['POST'])
    def prepare():
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
        if not click.validator(data):
            res = new_transaction.response()
            res['error'] = '-5'
            res['error_note'] = click.errors.get_error('-5')
            click.db.session.delete(new_transaction)
            click.db.session.commit()
            return jsonify(res), 200
        
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
        data = dict(request.form)
        if not check_in_req(data):
            return jsonify({"status" : "error"}), 400
        model = click.model
        transaction = model.query.filter_by(id = data.get('merchant_prepare_id')).first()
        if not transaction:
            res = {
                    "click_trans_id" : data['click_trans_id'],
                    "merchant_trans_id" : data['merchant_trans_id'],
                    "merchant_confirm_id" : data['merchant_prepare_id'],
                    "error" : data['error'],
                    "error_note" : data['error_note']
                }
            res['error'] = '-6'
            res['error_note'] = click.errors.get_error('-6')
            return jsonify(res), 200
        if data.get('error') == '-5017' or transaction.error == -9:
            click.callback(transaction)
            transaction.error = -9
            transaction.error_note = click.errors.get_error('-9')
            click.db.session.commit()
            res = transaction.response_confirm()
            return jsonify(res), 200
        if not check_hash_code_prepare(data, click.click_secret, transaction.id):
            res = transaction.response_confirm()
            res['error'] = '-1'
            res['error_note'] = click.errors.get_error('-1')
            return jsonify(res), 200
        if transaction.amount != float(data.get('amount')):
            res = transaction.response_confirm()
            res['error'] = '-2'
            res['error_note'] = click.errors.get_error('-2')
            return jsonify(res), 200
        if transaction.action == 1:
            res = transaction.response_confirm()
            res['error'] = '-4'
            res['error_note'] = click.errors.get_error('-4')
            return jsonify(res), 200
            
        transaction.error = 0
        transaction.error_note = click.errors.get_error('0')
        transaction.action = 1
        click.db.session.commit()
        click.callback(transaction)
        return jsonify(transaction.response_confirm()), 200
    return bp


