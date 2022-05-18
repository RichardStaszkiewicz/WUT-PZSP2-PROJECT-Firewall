from flask import Flask, jsonify, render_template, request
import os

# mocks
from rules import get_rules
from logs import get_logs


app = Flask(__name__)

rules = get_rules()


@app.route('/getRules', methods=['GET', 'POST'])
def update_rules():
    if request.method == 'POST':

        if request.args.get('action') == 'disableAll':
            for rule in rules:
                rule['is_active'] = False
            return 'ok'

        if request.args.get('action') == 'enableAll':
            for rule in rules:
                rule['is_active'] = True
            return 'ok'

        if request.args.get('action') == 'save':
            pass #code for save 
            return 'ok'

        rule_data = request.get_json()
        for i in range(len(rules)):
            if rules[i]['id'] == rule_data['id']:
                rules[i] = rule_data
                return 'ok'

        rules.append(rule_data)
        return 'ok'

    if request.method == 'GET':
        return jsonify(rules)


@app.route('/')
def home():
    logs = get_logs()
    return render_template('index.html', logs=logs, rules=rules)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
