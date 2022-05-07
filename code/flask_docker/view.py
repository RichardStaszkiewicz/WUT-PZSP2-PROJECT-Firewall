from flask import Flask, redirect, render_template, request, url_for
import os

# mocks
from rules import get_rules
from static.mocks.logs import get_logs


app = Flask(__name__)

rules = get_rules()


@app.route('/getRules', methods=['GET', 'POST'])
def update_rules():
    if request.method == 'POST':
        rule_data = request.get_json()
        rules.append(rule_data)

    return redirect(url_for('/'))


@app.route('/')
def home():
    logs = get_logs()
    return render_template('index.html', logs=logs, rules=rules)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
