from flask import Flask
from db import init_app

app = Flask(__name__)
app.secret_key = 'mysecretkey123'
init_app(app)

@app.route('/')
def index():
    return 'hello this is dailyfuel'

if __name__ == '__main__':
    with app.app_context():
        from db import init_db
        init_db()
    app.run(debug=True)