from main.config import db, app
from main.config import blueprint

if __name__ == "__main__":
    # create tables only once
    db.create_all(app=app)
    app.register_blueprint(blueprint)
    app.run(debug=True)
