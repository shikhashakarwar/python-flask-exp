import os
from flask import Flask, jsonify
# from app import routes

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_key= "dev", DATABASE= os.path.join(app.instance_path, "quiz_db"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    @app.route('/index')
    def index():
        return "Good to work on python"

    @app.route('/home')
    def home():
        return jsonify({"status": "some test"})
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app