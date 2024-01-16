from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    sql_query = text("SELECT * FROM cafe")
    result = db.session.execute(sql_query)
    all_cafes = result.fetchall()
    return render_template('index.html', cafes=all_cafes)

if __name__=="__main__":
    app.run(debug=True)