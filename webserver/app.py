#   --coding:utf-8 --

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
import models

basepath = path.abspath(path.dirname(__file__))
dburl = "sqlite:///" + path.join(basepath.split("\webserver")[0],"web\\network.db")
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= dburl
db = SQLAlchemy(app)


@app.route("/")
def showdata():
	results = tuple(db.session.query(models.NetDB).all())
	return render_template("index.html",records=results)


if	__name__ == "__main__":
	app.run(debug=True)

