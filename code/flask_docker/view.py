from flask import Flask, render_template, request
import os

# mocks
from static.mocks.rules import getRules


app = Flask(__name__)


@app.route('/')
def rules():
    rules = getRules()
    return render_template('rules.html', messages=rules)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
