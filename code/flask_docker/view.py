import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import subprocess

from rules import get_rules
from logs import get_logs


app = Flask(__name__)

RULES = get_rules()
LOGS = get_logs()
IS_LOGIN = False
USERNAME = 'admin'
PASSWORD = 'admin'

@app.route('/getRules', methods=['GET', 'POST'])
def update_rules():
    global LOGS

    if request.method == 'POST':

        if request.args.get('action') == 'disableAll':
            for rule in rules:
                rule['is_active'] = False
            return 'ok'

        if request.args.get('action') == 'enableAll':
            for rule in rules:
                rule['is_active'] = True
            return 'ok'

        if request.args.get('action') == "fetchLogs":
            LOGS = get_logs()
            return 'ok'

        if request.args.get('action') == 'save':
            rules_data = request.get_json()

            with open("../../data/rules.json", 'w') as file:
                data = {}
                data["rules"] = rules_data
                json.dump(data, file) 

            subprocess.call("./RunFifoScript.sh")
            return 'ok'

        rule_data = request.get_json()

        for i in range(len(RULES)):
            if RULES[i]['id'] == rule_data['id']:
                RULES[i] = rule_data
                return 'ok'
        
        RULES.append(rule_data)
        return 'ok'

    if request.method == 'GET':
        return jsonify(RULES)


@app.route('/home')
def home():
    if not IS_LOGIN:
        return redirect(url_for('login'))
    return render_template('index.html', logs=LOGS, rules=RULES)


@app.route('/', methods=['GET', 'POST'])
def login():
    global IS_LOGIN
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME or request.form['password'] != PASSWORD:
            error = 'Invalid Credentials. Please try again.'
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            IS_LOGIN = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context='adhoc')
