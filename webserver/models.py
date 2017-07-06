#     --coding:utf-8 --
from app import db


class	NetDB(db.Model):
		__tablename__ = "network"
		id = db.Column(db.Integer,primary_key=True,autoincrement=True)
		times = db.Column(db.String,nullable=False)
		server_name = db.Column(db.String,nullable=False)
		ip_addr = db.Column(db.String,nullable=False)
		status = db.Column(db.String,nullable=False)
		services = db.Column(db.String,nullable=True)

