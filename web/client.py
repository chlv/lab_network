#   --coding:utf-8 --

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import sessionmaker
from os import path
import subprocess
import time
global OURAY_NET,OURAY_SER,VALFS_NET,VALFS_SER,SCR_NET

basedir = path.abspath(path.dirname(__file__))
dburl = "sqlite:///"+path.join(basedir,"network.db")
engine = create_engine(dburl,echo=True)
base = declarative_base()


class NetDB(base):
	__tablename__ = "network"
	id = Column(Integer,primary_key=True,autoincrement=True)
	times = Column(String,nullable=False)
	server_name = Column(String,nullable=False)
	ip_addr = Column(String,nullable=False)
	status = Column(String,nullable=False)
	services = Column(String,nullable=True)


def pingfunc(servername):
	cmd = ("ping",servername)
	try:
		subprocess.check_call(cmd,shell=True)
		result = "OK"
	except subprocess.CalledProcessError:
		result = "Ping Failed"
	finally:
		return result

def netusefunc(path):
	cmd = "net use y: " + path
	try:
		subprocess.check_call(cmd,shell=True)
		result = "OK"
	except subprocess.CalledProcessError:
		result = "File Mount Failed"
	finally:
		time.sleep(10)
		cmd = "net use y: /del"
		subprocess.check_call(cmd,shell=True)
		return result

def nowtime():
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def netstatus(servername,location):
	net_result = pingfunc(servername)
	if net_result == "Ping Failed":
		service_result = "No need to check"
	else:
		service_result = netusefunc(location)
	return (net_result,service_result)

def samerecord(servername,net,service=None):
	global OURAY_NET,OURAY_SER,VALFS_NET,VALFS_SER,SCR_NET
	if servername == "192.101.1.10":
		if OURAY_NET==net and OURAY_SER==service:
			return True
		else:
			OURAY_NET=net
			OURAY_SER=service
			return False
	elif servername == "192.101.1.200":
		if VALFS_NET==net and VALFS_SER==service:
			return True
		else:
			VALFS_NET=net
			VALFS_SER=service
			return False
	else:
		if SCR_NET==net:
			return True
		else:
			SCR_NET=net
			return False



if  __name__ == "__main__":
	count = 0    # must write first three records
	base.metadata.create_all(engine)
	OURAY_NET,OURAY_SER=ouray_net,ouray_service = netstatus("192.101.1.10","\\\\ouray\\swstack\\Tools")
	record1 = NetDB(times=nowtime(),server_name="Ouray",ip_addr="192.101.1.10",status=ouray_net,services=ouray_service)
	VALFS_NET,VALFS_SER=valfs_net,valfs_service = netstatus("192.101.1.200","\\\\valfs\\share\\chlv\\linux")
	record2 = NetDB(times=nowtime(),server_name="Valfs",ip_addr="192.101.1.200",status=valfs_net,services=valfs_service)
	SCR_NET=scrutinizer_net = pingfunc("10.227.0.57")
	record3 = NetDB(times=nowtime(),server_name="Scrutinizer",ip_addr="10.227.0.57",status=scrutinizer_net,services='Not Check')
	#OURAY_NET=ouray_net,OURAY_SER=ouray_service,VALFS_NET=valfs_net,VALFS_SER=valfs_service,SCR_NET=scrutinizer_net
	sessionclass = sessionmaker(bind=engine)
	session = sessionclass()
	session.add_all([record1,record2,record3])
	session.commit()
	while True:
		ouray_net,ouray_service = netstatus("192.101.1.10","\\\\ouray\\swstack\\Tools")
		if samerecord("192.101.1.10",ouray_net,ouray_service):
			pass
		else:
			record1 = NetDB(times=nowtime(),server_name="Ouray",ip_addr="192.101.1.10",status=ouray_net,services=ouray_service)
			session.add(record1)
		valfs_net,valfs_service = netstatus("192.101.1.200","\\\\valfs\\share\\chlv\\linux")
		if samerecord("192.101.1.200",valfs_net,valfs_service):
			pass
		else:
			record2 = NetDB(times=nowtime(),server_name="Valfs",ip_addr="192.101.1.200",status=valfs_net,services=valfs_service)
			session.add(record2)
		scrutinizer_net = pingfunc("10.227.0.57")
		if samerecord("Scrutinizer",scrutinizer_net):
			pass
		else:
			record3 = NetDB(times=nowtime(),server_name="Scrutinizer",ip_addr="10.227.0.57",status=scrutinizer_net,services="Not Check")
			session.add(record3)
		session.commit()
		time.sleep(5)






