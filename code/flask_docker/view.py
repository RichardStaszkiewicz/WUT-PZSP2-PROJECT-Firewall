from flask import Flask, render_template, request
import os

# mocks
from rules import get_rules
from static.mocks.logs import get_logs


app = Flask(__name__)


@app.route('/')
def home():
    rules = get_rules()
    logs = get_logs()
    return render_template('index.html', logs=logs, rules=rules)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
