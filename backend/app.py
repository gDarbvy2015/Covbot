from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def get_reply():  # put application's code here
    pass


if __name__ == '__main__':
    app.run()
