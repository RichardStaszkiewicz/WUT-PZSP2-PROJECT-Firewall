import json
from typing import Hashable
from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import subprocess
from time import sleep

from rules import get_rules
from logs import get_logs
# 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Hash'))
import Hash


app = Flask(__name__)

RULES = get_rules()
LOGS = get_logs()
IS_LOGIN = False
# USERNAME = 'admin'
# PASSWORD = 'admin'
FILEPATH = 'data/passwd.json'

@app.route('/getRules', methods=['GET', 'POST'])
def update_rules():
    global LOGS
    global IS_LOGIN

    if request.method == 'POST':

        if request.args.get('action') == 'disableAll':
            for rule in RULES:
                rule['is_active'] = 'false'
            return 'ok'

        if request.args.get('action') == 'enableAll':
            for rule in RULES:
                rule['is_active'] = 'true'
            return 'ok'

        if request.args.get('action') == "fetchLogs":
            LOGS = get_logs()
            return 'ok'

        if request.args.get('action') == "logout":
            IS_LOGIN = False
            return 'ok'
        
        if request.args.get('action') == 'save':
            rules_data = request.get_json()
            data = {}
            data["rules"] = rules_data

            with open("./data/rules.json", 'w') as file:
                json.dump(data, file, indent=2)

            sleep(1)
            subprocess.call("./code/RunFifoScript.sh")
            return 'ok'

        if request.args.get('action') == 'deleteRule':
            rule_to_delete = request.get_json()[0]
            RULES.remove(rule_to_delete)
            return 'ok'

        modified_rule = request.get_json()
        for i in range(len(RULES)):
            if RULES[i].get('id') == modified_rule['id']:
                RULES[i] = modified_rule
                return 'ok'
        RULES.append(modified_rule)
        return 'ok'

    if request.method == 'GET':
        return jsonify(RULES)


@app.route('/home')
def home():
    if not IS_LOGIN:
        return redirect(url_for('login'))
    return render_template('index.html', logs=LOGS, rules=RULES)


@app.route('/', methods=['GET', 'POST'])
def login():#https://pentestmonkey.net/blog/direnum
    global IS_LOGIN
    error = None
    if request.method == 'POST':
        # NEW
        if not Hash.is_password_correct(request.form['username'],request.form['password'], FILEPATH):
            error = 'Invalid Credentials. Please try again.'
        if Hash.is_password_correct(request.form['username'],request.form['password'], FILEPATH):
            IS_LOGIN = True
            return redirect(url_for('home')) 
        # OLD
        # if request.form['username'] != USERNAME or request.form['password'] != PASSWORD:
        #     error = 'Invalid Credentials. Please try again.'
        # if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
        #     IS_LOGIN = True
        #     return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, ssl_context='adhoc')
