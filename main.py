from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SECRET_KEY'] = 'abc'
db = SQLAlchemy()
db.init_app(app)


with app.app_context():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
    finally:
        db.session.close()


class AddCafe(FlaskForm):
    name = StringField("Cafe name",
                       validators=[DataRequired()])
    map_url = StringField("Nap URL",
                          validators=[DataRequired()])
    img_url = StringField("IMG URL",
                          validators=[DataRequired()])
    location = StringField("Location",
                           validators=[DataRequired()])
    has_sockets = StringField("If has sockets? 0 for no, 1 for yes",
                              validators=[DataRequired()])
    has_toilet = StringField("If has toilet? 0 for no, 1 for yes",
                             validators=[DataRequired()])
    has_wifi = StringField("If has free wifi? 0 for no, 1 for yes",
                           validators=[DataRequired()])
    can_take_call = StringField("If can U take calls? 0 for no, 1 for yes",
                                validators=[DataRequired()])
    seats = StringField("Avg. seats (example '20-40')",
                        validators=[DataRequired()])
    coffee_price = StringField("Avg. price for coffee",
                               validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    sql_query = text("SELECT * FROM cafe")
    result = db.session.execute(sql_query)
    all_cafes = result.fetchall()
    return render_template('home.html', cafes=all_cafes)


@app.route("/add", methods=["POST"])
def add_cafe():
    form = AddCafe()
    if form.validate_on_submit():
        sql_query = text("""
            INSERT INTO cafe (name, map_url, img_url, location, has_sockets,
                         has_toilet, has_wifi, can_take_calls,
                         seats, coffee_price)
            VALUES (:name, :map_url, :img_url, :location, :has_sockets,
                         :has_toilet, :has_wifi, :can_take_calls,
                         :seats, :coffee_price)
        """)
        db.session.execute(
            sql_query,
            {
                "name": form.name.data,
                "map_url": form.map_url.data,
                "img_url": form.img_url.data,
                "location": form.location.data,
                "has_sockets": form.has_sockets.data,
                "has_toilet": form.has_toilet.data,
                "has_wifi": form.has_wifi.data,
                "can_take_calls": form.can_take_call.data,
                "seats": form.seats.data,
                "coffee_price": form.coffee_price.data,
            }
        )
        db.session.commit()
        return jsonify(response={"success: Sucecessfully added new cafe."})
    return render_template('add.html', form=form)


@app.route("/delete/<int:caffee_id>", methods=["DELETE"])
def delete_cafe(caffee_id):
    delete_sql_query = text("DELETE FROM cafe WHERE id = :id")
    cafe = db.session.execute(delete_sql_query, {"id": caffee_id})
    if cafe:
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/all", methods=["GET"])
def all_cafes():
    sql_query = text("SELECT * FROM cafe")
    result = db.session.execute(sql_query)
    all_cafes = result.fetchall()

    cafes_dict_list = [
        {
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "can_take_calls": cafe.can_take_calls,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price
        }
        for cafe in all_cafes
    ]
    return jsonify({"cafes": cafes_dict_list})


if __name__ == "__main__":
    app.run(debug=True)
