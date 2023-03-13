from flask import Flask
from backend.endpoint.group.group import app_group
from backend.endpoint.group_detail.group_detail import app_group_detail
from flask_cors import CORS


# init Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# register blueprints
app.register_blueprint(app_group, url_prefix="/group")
app.register_blueprint(app_group_detail, url_prefix="/group_detail")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
